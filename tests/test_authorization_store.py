from datetime import datetime, timedelta, timezone
from uuid import uuid4

from kernel.authority import SQLiteAuthorizationStore, issue_authorization
from kernel.durability import SQLiteEventStore
from kernel.models import GovernanceDecision, Proposal


def make_authorization():
    proposal = Proposal(
        id=uuid4(),
        request_id=uuid4(),
        principal_id=uuid4(),
        operation="file.read",
        resource="local:test",
        parameters={"path": "example.txt"},
    )
    return issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted"),
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        timedelta(minutes=1),
    )


def test_authorization_record_round_trips_through_sqlite() -> None:
    store = SQLiteEventStore()
    try:
        authorization = make_authorization()
        durable = SQLiteAuthorizationStore(store)
        durable.save(authorization)
        assert durable.get(authorization.id) == authorization
    finally:
        store.close()


def test_authorization_record_survives_store_reopen(tmp_path) -> None:
    database = tmp_path / "kernel.db"
    authorization = make_authorization()

    store = SQLiteEventStore(str(database))
    try:
        SQLiteAuthorizationStore(store).save(authorization)
    finally:
        store.close()

    reopened = SQLiteEventStore(str(database))
    try:
        assert SQLiteAuthorizationStore(reopened).get(authorization.id) == authorization
    finally:
        reopened.close()


def test_authorization_record_save_is_idempotent() -> None:
    store = SQLiteEventStore()
    try:
        authorization = make_authorization()
        durable = SQLiteAuthorizationStore(store)
        durable.save(authorization)
        durable.save(authorization)
        assert durable.get(authorization.id) == authorization
    finally:
        store.close()


def test_conflicting_authorization_save_is_rejected() -> None:
    store = SQLiteEventStore()
    try:
        authorization = make_authorization()
        durable = SQLiteAuthorizationStore(store)
        durable.save(authorization)

        conflicting = authorization.__class__(
            id=authorization.id,
            principal_id=authorization.principal_id,
            proposal_id=authorization.proposal_id,
            operation=authorization.operation,
            resource="local:other",
            issued_at=authorization.issued_at,
            expires_at=authorization.expires_at,
            parameters_fingerprint=authorization.parameters_fingerprint,
        )
        import pytest

        with pytest.raises(ValueError, match="conflicting authority"):
            durable.save(conflicting)
        assert durable.get(authorization.id) == authorization
    finally:
        store.close()
