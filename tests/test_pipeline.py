from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from kernel import process
from kernel.authority import (
    AuthorizationError,
    RevocationRegistry,
    enforce_authorization,
    issue_authorization,
)
from kernel.durability import SQLiteEventStore
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


def test_connected_allow_path_persists_event_and_state():
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
        assert event.sequence == 1
        assert event.event_type == "execution.succeeded"
        assert adapter.calls == 1
        assert store.get_state(event.payload["request_id"])[1] == event.sequence
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
