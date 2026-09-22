from datetime import datetime, timedelta, timezone
import json
from uuid import uuid4

import pytest

from kernel import process
from kernel.authority import (
    AuthorizationError,
    RevocationRegistry,
    enforce_authorization,
    issue_authorization,
)
from kernel.durability import AuthorizationIssuanceError, SQLiteEventStore
from kernel.intake import build_proposal, receive_request
from kernel.models import GovernanceDecision, Outcome, Principal


class Allow:
    def evaluate(self, proposal, context):
        return GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")


class Deny:
    def evaluate(self, proposal, context):
        return GovernanceDecision("DENY", proposal.id, "test-policy", "denied")


class Adapter:
    def __init__(self):
        self.calls = 0

    def execute(self, authorization, parameters):
        self.calls += 1
        return Outcome(uuid4(), "SUCCEEDED", {"accepted": True})


def test_connected_allow_path_persists_authorization_lineage():
    store = SQLiteEventStore()
    adapter = Adapter()
    try:
        event = process(
            Principal(uuid4(), "human"),
            operation="test.execute",
            resource="local:test",
            parameters={"x": 1},
            governance=Allow(),
            adapter=adapter,
            store=store,
        )
        events = store.all_events()
        assert event.sequence == 3
        assert events[0][2] == "authorization.issued"
        assert events[1][2] == "execution.attempted"
        assert events[2][2] == "execution.succeeded"
        assert event.payload["authorization_issued_sequence"] == events[0][0]
        assert events[1][4] and "attempt_id" in events[1][4]
        assert event.payload["attempt_id"] == json.loads(events[1][4])["attempt_id"]
        authorization_id = event.payload["authorization_id"]
        assert store.get_authorization(authorization_id) is not None
        assert adapter.calls == 1
        assert store.get_state(event.payload["request_id"])[1] == event.sequence
    finally:
        store.close()


def test_authorization_record_alone_does_not_grant_authority():
    principal = Principal(uuid4(), "human")
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    now = datetime.now(timezone.utc)
    authorization = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "v1", "permitted"),
        now,
        timedelta(minutes=1),
    )
    store = SQLiteEventStore()
    try:
        store.save_authorization(authorization)
        unrelated_request = receive_request(
            principal,
            operation="test.delete",
            resource="local:other",
            parameters={},
        )
        unrelated_proposal = build_proposal(unrelated_request)
        with pytest.raises(AuthorizationError):
            enforce_authorization(
                authorization, unrelated_proposal, now
            )
    finally:
        store.close()


def test_denial_never_reaches_adapter():
    store = SQLiteEventStore()
    adapter = Adapter()
    try:
        event = process(
            Principal(uuid4(), "human"),
            operation="test.execute",
            resource="local:test",
            parameters={},
            governance=Deny(),
            adapter=adapter,
            store=store,
        )
        assert event.event_type == "request.denied"
        assert adapter.calls == 0
        assert len(store.all_events()) == 1
    finally:
        store.close()


def test_revoked_authorization_blocks_effect():
    principal = Principal(uuid4(), "human")
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    now = datetime.now(timezone.utc)
    authorization = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "v1", "permitted"),
        now,
        timedelta(minutes=1),
    )
    registry = RevocationRegistry()
    registry.revoke(authorization.id)
    with pytest.raises(AuthorizationError):
        enforce_authorization(authorization, proposal, now, registry)


def test_event_and_state_rollback_together():
    store = SQLiteEventStore()
    try:
        with pytest.raises(Exception):
            store.append_with_state(
                event_id=str(uuid4()),
                event_type="test.atomicity",
                timestamp=datetime.now(timezone.utc).isoformat(),
                payload={"ok": True},
                subject=str(uuid4()),
                state={"not_json": float("nan")},
            )
        assert store.all_events() == []
        assert store.get_state("missing") is None
    finally:
        store.close()


def test_authorization_issuance_is_idempotent():
    principal = Principal(uuid4(), "human")
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    now = datetime.now(timezone.utc)
    authorization = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "v1", "permitted"),
        now,
        timedelta(minutes=1),
    )
    store = SQLiteEventStore()
    try:
        first = store.append_authorization_issued(
            authorization,
            event_id=str(uuid4()),
            timestamp=now.isoformat(),
            request_id=str(request.id),
            correlation_id=str(request.id),
            provenance={"source": "test"},
        )
        second = store.append_authorization_issued(
            authorization,
            event_id=str(uuid4()),
            timestamp=now.isoformat(),
            request_id=str(request.id),
            correlation_id=str(request.id),
            provenance={"source": "test"},
        )
        assert second == first
        assert len(store.all_events()) == 1
    finally:
        store.close()


def test_conflicting_authorization_issuance_is_rejected():
    principal = Principal(uuid4(), "human")
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    now = datetime.now(timezone.utc)
    authorization = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "v1", "permitted"),
        now,
        timedelta(minutes=1),
    )
    store = SQLiteEventStore()
    try:
        store.append_authorization_issued(
            authorization,
            event_id=str(uuid4()),
            timestamp=now.isoformat(),
            request_id=str(request.id),
            correlation_id=str(request.id),
            provenance={"source": "test"},
        )
        with pytest.raises(AuthorizationIssuanceError):
            store.append_authorization_issued(
                authorization,
                event_id=str(uuid4()),
                timestamp=now.isoformat(),
                request_id=str(uuid4()),
                correlation_id=str(request.id),
                provenance={"source": "test"},
            )
        assert len(store.all_events()) == 1
    finally:
        store.close()


class RaisingAdapter:
    def execute(self, authorization, parameters):
        raise RuntimeError("simulated interruption after effect invocation")


def test_adapter_failure_leaves_attempt_evidence_durable():
    store = SQLiteEventStore()
    try:
        with pytest.raises(RuntimeError, match="simulated interruption"):
            process(
                Principal(uuid4(), "human"),
                operation="test.execute",
                resource="local:test",
                parameters={},
                governance=Allow(),
                adapter=RaisingAdapter(),
                store=store,
            )
        events = store.all_events()
        assert [row[2] for row in events] == [
            "authorization.issued",
            "execution.attempted",
        ]
        attempt = json.loads(events[1][4])
        assert attempt["authorization_issued_sequence"] == events[0][0]
        assert attempt["attempt_id"]
        assert store.get_state(attempt["request_id"]) is None
    finally:
        store.close()
