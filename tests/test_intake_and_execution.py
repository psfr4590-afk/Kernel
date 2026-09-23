from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from kernel.authority import issue_authorization
from kernel.execution import ExecutionProtocolError, execute
from kernel.intake import build_proposal, capture_context, receive_request
from kernel.models import GovernanceDecision, Outcome, Principal


class RecordingAdapter:
    def __init__(self):
        self.calls = 0

    def execute(self, authorization, parameters):
        self.calls += 1
        return Outcome(uuid4(), "SUCCEEDED", {"parameters": dict(parameters)})


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


class InvalidStatusAdapter:
    def execute(self, authorization, parameters):
        return Outcome(uuid4(), "SUCCEEDED_WITH_A_SURPRISE", {})


class InvalidEvidenceAdapter:
    def execute(self, authorization, parameters):
        return Outcome(uuid4(), "SUCCEEDED", ["not", "a", "mapping"])


def _authorized_execution():
    principal = Principal(uuid4(), "human", True)
    request = receive_request(
        principal, operation="test.execute", resource="local:test", parameters={}
    )
    proposal = build_proposal(request)
    now = datetime.now(timezone.utc)
    auth = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted"),
        now,
        timedelta(minutes=1),
    )
    return auth, proposal, now


def test_invalid_adapter_status_is_rejected_after_attempt():
    auth, proposal, now = _authorized_execution()
    attempts = []

    with pytest.raises(ExecutionProtocolError, match="unsupported terminal status"):
        execute(
            auth,
            proposal,
            InvalidStatusAdapter(),
            now=now,
            on_attempt=lambda attempt_id: attempts.append(attempt_id),
        )

    assert len(attempts) == 1


def test_invalid_adapter_evidence_is_rejected_after_attempt():
    auth, proposal, now = _authorized_execution()
    attempts = []

    with pytest.raises(ExecutionProtocolError, match="non-mapping evidence"):
        execute(
            auth,
            proposal,
            InvalidEvidenceAdapter(),
            now=now,
            on_attempt=lambda attempt_id: attempts.append(attempt_id),
        )

    assert len(attempts) == 1


def test_execution_is_blocked_after_authorization_expiry():
    auth, proposal, now = _authorized_execution()
    expired_at = auth.expires_at + timedelta(microseconds=1)
    adapter = RecordingAdapter()

    outcome = execute(auth, proposal, adapter, now=expired_at)

    assert outcome.status == "BLOCKED"
    assert adapter.calls == 0
