"""First connected Kernel vertical slice."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping

from kernel.authority import RevocationRegistry, issue_authorization
from kernel.durability import SQLiteEventStore
from kernel.execution import execute
from kernel.intake import build_proposal, capture_context, receive_request
from kernel.interfaces import ExecutionAdapter, GovernanceEvaluator, IdentityProvider
from kernel.models import Event, Principal, new_id, utc_now


def process(
    principal: Principal | None = None,
    *,
    operation: str,
    resource: str,
    parameters: Mapping[str, Any],
    governance: GovernanceEvaluator,
    adapter: ExecutionAdapter,
    store: SQLiteEventStore,
    revocations: RevocationRegistry | None = None,
    identity_provider: IdentityProvider | None = None,
    idempotency_key: str | None = None,
):
    """Process one request through the identity, authority, and effect boundaries."""
    if identity_provider is not None:
        if principal is not None:
            raise ValueError("provide either principal or identity_provider, not both")
        principal = identity_provider.authenticate()
    if principal is None:
        raise ValueError("principal or identity_provider is required")

    request = receive_request(
        principal,
        operation=operation,
        resource=resource,
        parameters=parameters,
        idempotency_key=idempotency_key,
    )
    existing_request_id, _, created = store.claim_operation(
        principal_id=str(principal.id),
        idempotency_key=request.idempotency_key if idempotency_key is None else idempotency_key,
        request_id=str(request.id),
        operation=operation,
        resource=resource,
        parameters=parameters,
        timestamp=request.received_at.isoformat(),
        correlation_id=str(request.id),
        provenance={"source": "kernel.pipeline"},
    )
    if not created:
        existing_event = store.latest_event_for_request(existing_request_id)
        if existing_event is None:
            raise RuntimeError("claimed operation has no durable evidence")
        sequence, event_id, event_type, timestamp, payload = existing_event
        import json
        return Event(
            id=__import__("uuid").UUID(event_id),
            sequence=sequence,
            event_type=event_type,
            timestamp=__import__("datetime").datetime.fromisoformat(timestamp),
            payload=json.loads(payload),
            principal_id=principal.id,
            request_id=__import__("uuid").UUID(existing_request_id),
            correlation_id=__import__("uuid").UUID(existing_request_id),
            provenance={"source": "kernel.pipeline"},
        )

    proposal = build_proposal(request)
    context = capture_context(principal, resource)
    decision = governance.evaluate(proposal, context)

    now = utc_now()
    if decision.decision != "ALLOW":
        event = Event(
            id=new_id(),
            sequence=0,
            event_type="request.denied",
            timestamp=now,
            principal_id=principal.id,
            request_id=request.id,
            correlation_id=request.id,
            provenance={"source": "kernel.pipeline"},
            payload={
                "request_id": str(request.id),
                "proposal_id": str(proposal.id),
                "principal_id": str(principal.id),
                "reason": decision.reason,
            },
        )
        sequence = store.append_with_state(
            event_id=str(event.id),
            event_type=event.event_type,
            timestamp=event.timestamp.isoformat(),
            payload=event.payload,
            subject=str(request.id),
            state={"status": "DENIED"},
            schema_version=event.schema_version,
            principal_id=str(event.principal_id),
            request_id=str(event.request_id),
            causation_id=str(event.causation_id) if event.causation_id else None,
            correlation_id=str(event.correlation_id) if event.correlation_id else None,
            provenance=event.provenance,
        )
        return Event(**{**event.__dict__, "sequence": sequence})

    authorization = issue_authorization(
        proposal, decision, now, timedelta(minutes=1)
    )
    authorization_sequence = store.append_authorization_issued(
        authorization,
        event_id=str(new_id()),
        timestamp=now.isoformat(),
        request_id=str(request.id),
        correlation_id=str(request.id),
        provenance={"source": "kernel.pipeline"},
    )
    def record_attempt(attempt_id):
        attempt_event = Event(
            id=new_id(),
            sequence=0,
            event_type="execution.attempted",
            timestamp=utc_now(),
            principal_id=principal.id,
            request_id=request.id,
            correlation_id=request.id,
            provenance={"source": "kernel.pipeline"},
            payload={
                "request_id": str(request.id),
                "proposal_id": str(proposal.id),
                "authorization_id": str(authorization.id),
                "attempt_id": str(attempt_id),
                "principal_id": str(principal.id),
                "authorization_issued_sequence": authorization_sequence,
            },
        )
        store.append(
            event_id=str(attempt_event.id),
            event_type=attempt_event.event_type,
            timestamp=attempt_event.timestamp.isoformat(),
            payload=attempt_event.payload,
            schema_version=attempt_event.schema_version,
            principal_id=str(attempt_event.principal_id),
            request_id=str(attempt_event.request_id),
            causation_id=str(attempt_event.causation_id) if attempt_event.causation_id else None,
            correlation_id=str(attempt_event.correlation_id) if attempt_event.correlation_id else None,
            provenance=attempt_event.provenance,
        )

    outcome = execute(
        authorization,
        proposal,
        adapter,
        now=now,
        revocations=revocations,
        on_attempt=record_attempt,
    )
    event = Event(
        id=new_id(),
        sequence=0,
        event_type=f"execution.{outcome.status.lower()}",
        timestamp=utc_now(),
        principal_id=principal.id,
        request_id=request.id,
        correlation_id=request.id,
        provenance={"source": "kernel.pipeline"},
        payload={
            "request_id": str(request.id),
            "proposal_id": str(proposal.id),
            "authorization_id": str(authorization.id),
            "attempt_id": str(outcome.attempt_id),
            "principal_id": str(principal.id),
            "outcome": outcome.status,
            "authorization_issued_sequence": authorization_sequence,
        },
    )
    sequence = store.append_with_state(
        event_id=str(event.id),
        event_type=event.event_type,
        timestamp=event.timestamp.isoformat(),
        payload=event.payload,
        subject=str(request.id),
        state={"status": outcome.status},
        schema_version=event.schema_version,
        principal_id=str(event.principal_id),
        request_id=str(event.request_id),
        causation_id=str(event.causation_id) if event.causation_id else None,
        correlation_id=str(event.correlation_id) if event.correlation_id else None,
        provenance=event.provenance,
    )
    return Event(**{**event.__dict__, "sequence": sequence})
