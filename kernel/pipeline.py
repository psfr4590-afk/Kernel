"""First connected Kernel vertical slice."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping

from kernel.authority import RevocationRegistry, issue_authorization
from kernel.durability import SQLiteEventStore
from kernel.execution import execute
from kernel.intake import build_proposal, capture_context, receive_request
from kernel.interfaces import ExecutionAdapter, GovernanceEvaluator
from kernel.models import Event, Principal, utc_now


def process(
    principal: Principal,
    *,
    operation: str,
    resource: str,
    parameters: Mapping[str, Any],
    governance: GovernanceEvaluator,
    adapter: ExecutionAdapter,
    store: SQLiteEventStore,
    revocations: RevocationRegistry | None = None,
):
    """Process one request through the authority and effect boundaries."""
    request = receive_request(
        principal,
        operation=operation,
        resource=resource,
        parameters=parameters,
    )
    proposal = build_proposal(request)
    context = capture_context(principal, resource)
    decision = governance.evaluate(proposal, context)

    now = utc_now()
    if decision.decision != "ALLOW":
        event = Event(
            id=__import__("kernel.models", fromlist=["new_id"]).new_id(),
            sequence=0,
            event_type="request.denied",
            timestamp=now,
            payload={
                "request_id": str(request.id),
                "proposal_id": str(proposal.id),
                "principal_id": str(principal.id),
                "reason": decision.reason,
            },
        )
        sequence = store.append(
            event_id=str(event.id),
            event_type=event.event_type,
            timestamp=event.timestamp.isoformat(),
            payload=event.payload,
        )
        return event.__class__(**{**event.__dict__, "sequence": sequence})

    authorization = issue_authorization(
        proposal, decision, now, timedelta(minutes=1)
    )
    outcome = execute(
        authorization,
        proposal,
        adapter,
        now=now,
        revocations=revocations,
    )
    event = Event(
        id=__import__("kernel.models", fromlist=["new_id"]).new_id(),
        sequence=0,
        event_type=f"execution.{outcome.status.lower()}",
        timestamp=utc_now(),
        payload={
            "request_id": str(request.id),
            "proposal_id": str(proposal.id),
            "authorization_id": str(authorization.id),
            "attempt_id": str(outcome.attempt_id),
            "principal_id": str(principal.id),
            "outcome": outcome.status,
        },
    )
    sequence = store.append_with_state(
        event_id=str(event.id),
        event_type=event.event_type,
        timestamp=event.timestamp.isoformat(),
        payload=event.payload,
        subject=str(request.id),
        state={"status": outcome.status, "event_sequence": "pending"},
    )
    return event.__class__(**{**event.__dict__, "sequence": sequence})
