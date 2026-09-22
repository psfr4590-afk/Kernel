"""Contract-level tests for the first vertical slice boundaries."""

from datetime import datetime, timezone
from uuid import uuid4

from kernel.models import Context, GovernanceDecision, Proposal


def test_governance_contract_is_explicit():
    proposal_id = uuid4()
    proposal = Proposal(
        id=proposal_id,
        request_id=uuid4(),
        principal_id=uuid4(),
        operation="test.operation",
        resource="test.resource",
        parameters={},
    )
    context = Context(
        id=uuid4(),
        principal_id=proposal.principal_id,
        resource=proposal.resource,
        captured_at=datetime.now(timezone.utc),
    )
    decision = GovernanceDecision("DENY", proposal.id, "deferred", "not evaluated")
    assert decision.proposal_id == proposal.id
    assert context.principal_id == proposal.principal_id
