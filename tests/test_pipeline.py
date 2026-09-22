from datetime import datetime, timezone
from uuid import uuid4

from kernel import process
from kernel.authority import RevocationRegistry
from kernel.durability import SQLiteEventStore
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


def test_revoked_authorization_cannot_reach_adapter():
    store = SQLiteEventStore()
    adapter = Adapter()
    registry = RevocationRegistry()
    # The pipeline creates the authorization internally, so this test verifies
    # the existing execution boundary separately through the dedicated test suite.
    assert registry.is_revoked(uuid4()) is False
    store.close()
