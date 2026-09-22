from datetime import datetime, timedelta, timezone
from uuid import uuid4

from kernel.authority import issue_authorization
from kernel.execution import execute
from kernel.intake import build_proposal, capture_context, receive_request
from kernel.models import GovernanceDecision, Principal


class RecordingAdapter:
    def __init__(self):
        self.calls = 0

    def execute(self, authorization, parameters):
        self.calls += 1
        return type("Outcome", (), {})() if False else __import__("kernel.models", fromlist=["Outcome"]).Outcome(
            uuid4(), "SUCCEEDED", {"parameters": dict(parameters)}
        )


def test_request_to_execution_boundary():
    principal = Principal(uuid4(), "human", True)
    request = receive_request(
        principal,
        operation="test.execute",
        resource="local:test",
        parameters={"value": 7},
    )
    proposal = build_proposal(request)
    context = capture_context(principal, proposal.resource)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    now = datetime.now(timezone.utc)
    auth = issue_authorization(proposal, decision, now, timedelta(minutes=1))
    adapter = RecordingAdapter()

    outcome = execute(auth, proposal, adapter, now=now)

    assert context.principal_id == principal.id
    assert outcome.status == "SUCCEEDED"
    assert adapter.calls == 1


def test_execution_is_blocked_after_revocation():
    principal = Principal(uuid4(), "human", True)
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    now = datetime.now(timezone.utc)
    auth = issue_authorization(proposal, decision, now, timedelta(minutes=1))

    from kernel.authority import RevocationRegistry
    registry = RevocationRegistry()
    registry.revoke(auth.id)

    adapter = RecordingAdapter()
    outcome = execute(auth, proposal, adapter, now=now, revocations=registry)

    assert outcome.status == "BLOCKED"
    assert adapter.calls == 0
