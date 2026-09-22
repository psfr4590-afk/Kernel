from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from kernel.authority import AuthorizationError, enforce_authorization, issue_authorization
from kernel.models import GovernanceDecision, Proposal


def make_proposal() -> Proposal:
    return Proposal(
        id=uuid4(),
        request_id=uuid4(),
        principal_id=uuid4(),
        operation="file.read",
        resource="local:test",
        parameters={"path": "example.txt"},
    )


def test_allow_creates_bounded_authorization():
    proposal = make_proposal()
    now = datetime.now(timezone.utc)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    auth = issue_authorization(proposal, decision, now, timedelta(minutes=1))

    enforce_authorization(auth, proposal, now)
    assert auth.operation == proposal.operation
    assert auth.resource == proposal.resource


@pytest.mark.parametrize(
    "change",
    [
        {"principal_id": uuid4()},
        {"operation": "file.write"},
        {"resource": "local:other"},
        {"proposal_id": uuid4()},
    ],
)
def test_authorization_rejects_scope_or_identity_mismatch(change):
    proposal = make_proposal()
    now = datetime.now(timezone.utc)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    auth = issue_authorization(proposal, decision, now, timedelta(minutes=1))
    altered = auth.__class__(**{**auth.__dict__, **change})

    with pytest.raises(AuthorizationError):
        enforce_authorization(altered, proposal, now)


def test_expired_authorization_is_rejected():
    proposal = make_proposal()
    issued = datetime.now(timezone.utc)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    auth = issue_authorization(proposal, decision, issued, timedelta(seconds=1))

    with pytest.raises(AuthorizationError):
        enforce_authorization(auth, proposal, issued + timedelta(seconds=1))


def test_denial_cannot_issue_authorization():
    proposal = make_proposal()
    now = datetime.now(timezone.utc)
    decision = GovernanceDecision("DENY", proposal.id, "test-policy", "denied")

    with pytest.raises(AuthorizationError):
        issue_authorization(proposal, decision, now, timedelta(minutes=1))


def test_authorization_rejects_modified_parameters():
    proposal = make_proposal()
    now = datetime.now(timezone.utc)
    decision = GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted")
    auth = issue_authorization(proposal, decision, now, timedelta(minutes=1))
    altered = proposal.__class__(
        **{**proposal.__dict__, "parameters": {"path": "different.txt"}}
    )

    with pytest.raises(AuthorizationError):
        enforce_authorization(auth, altered, now)
