from datetime import datetime, timezone
from uuid import uuid4

import pytest

from kernel.authority import SQLiteRevocationRegistry
from kernel.authority import AuthorizationError, enforce_authorization, issue_authorization
from kernel.durability import SQLiteEventStore
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


def test_revocation_survives_registry_recreation():
    store = SQLiteEventStore()
    registry = SQLiteRevocationRegistry(store)
    authorization_id = uuid4()
    registry.revoke(
        authorization_id,
        datetime.now(timezone.utc).isoformat(),
        "security response",
        event_id=uuid4(),
    )

    recreated = SQLiteRevocationRegistry(store)
    assert recreated.is_revoked(authorization_id)
    events = store.all_events()
    assert len(events) == 1
    assert events[0][2] == "authorization.revoked"


def test_durable_revocation_blocks_authorization():
    store = SQLiteEventStore()
    registry = SQLiteRevocationRegistry(store)
    proposal = make_proposal()
    now = datetime.now(timezone.utc)
    authorization = issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted"),
        now,
        __import__("datetime").timedelta(minutes=1),
    )
    registry.revoke(
        authorization.id,
        now.isoformat(),
        "security response",
        event_id=uuid4(),
        principal_id=proposal.principal_id,
        request_id=proposal.request_id,
    )

    with pytest.raises(AuthorizationError, match="revoked"):
        enforce_authorization(authorization, proposal, now, registry)
