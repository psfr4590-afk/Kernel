from datetime import datetime, timezone
from uuid import uuid4

import pytest

from kernel.durability import (
    CanonicalJSONError,
    SQLiteEventStore,
    canonical_json,
    replay_request_state,
)


def test_canonical_json_is_deterministic():
    assert canonical_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'


def test_canonical_json_rejects_non_finite_numbers():
    with pytest.raises(CanonicalJSONError):
        canonical_json({"value": float("nan")})


def test_sqlite_event_store_assigns_durable_sequence():
    store = SQLiteEventStore()
    try:
        first = store.append(
            event_id=str(uuid4()),
            event_type="test.created",
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload={"value": 1},
        )
        second = store.append(
            event_id=str(uuid4()),
            event_type="test.completed",
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload={"value": 2},
        )
        assert second > first
        assert [row[0] for row in store.all_events()] == [first, second]
    finally:
        store.close()


def test_state_can_be_reconstructed_from_event_history():
    store = SQLiteEventStore()
    try:
        request_id = str(uuid4())
        store.append(
            event_id=str(uuid4()),
            event_type="request.denied",
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload={"request_id": request_id, "reason": "policy"},
        )
        state = replay_request_state(store.all_events(), request_id)
        assert state == {"status": "DENIED", "event_sequence": 1}
    finally:
        store.close()


def test_denial_state_is_materialized_with_event() -> None:
    from kernel import process
    from kernel.authority import RevocationRegistry
    from kernel.models import GovernanceDecision, Principal, new_id

    class Deny:
        def evaluate(self, proposal, context):
            return GovernanceDecision(
                decision="DENY",
                proposal_id=proposal.id,
                policy_version="test-1",
                reason="denied",
            )

    class Adapter:
        def execute(self, authorization, proposal):
            raise AssertionError("denied request reached execution")

    store = SQLiteEventStore()
    principal = Principal(id=new_id(), kind="test")
    event = process(
        principal,
        operation="test",
        resource="resource",
        parameters={},
        governance=Deny(),
        adapter=Adapter(),
        store=store,
        revocations=RevocationRegistry(),
    )

    assert event.event_type == "request.denied"
    assert store.get_state(str(event.request_id)) == ('{"status":"DENIED"}', event.sequence)


def test_state_sequence_must_not_move_backwards() -> None:
    store = SQLiteEventStore()
    first = store.append_with_state(
        event_id="event-1",
        event_type="execution.succeeded",
        timestamp="2026-01-01T00:00:00+00:00",
        payload={"request_id": "request-1"},
        subject="request-1",
        state={"status": "SUCCEEDED"},
    )
    store._connection.execute(
        "UPDATE state SET event_sequence=? WHERE subject=?",
        (first + 100, "request-1"),
    )
    store._connection.commit()

    from kernel.durability import StateSequenceError

    with pytest.raises(StateSequenceError):
        store.append_with_state(
            event_id="event-2",
            event_type="execution.failed",
            timestamp="2026-01-01T00:00:01+00:00",
            payload={"request_id": "request-1"},
            subject="request-1",
            state={"status": "FAILED"},
        )


def test_file_backed_store_survives_close_and_reopen(tmp_path) -> None:
    database = tmp_path / "kernel.db"
    store = SQLiteEventStore(str(database))
    request_id = str(uuid4())
    try:
        sequence = store.append(
            event_id=str(uuid4()),
            event_type="request.denied",
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload={"request_id": request_id, "reason": "policy"},
        )
        assert sequence == 1
    finally:
        store.close()

    reopened = SQLiteEventStore(str(database))
    try:
        assert len(reopened.all_events()) == 1
        assert replay_request_state(reopened.all_events(), request_id) == {
            "status": "DENIED",
            "event_sequence": 1,
        }
    finally:
        reopened.close()


def test_event_integrity_hash_is_deterministic_and_detects_payload_tampering():
    from kernel.durability import event_integrity_hash, verify_event_integrity

    payload = {"request_id": "request-1", "value": 7}
    kwargs = {
        "event_id": "event-1",
        "event_type": "test.event",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "payload": payload,
        "request_id": "request-1",
        "provenance": {"source": "test"},
    }
    first = event_integrity_hash(**kwargs)
    second = event_integrity_hash(**kwargs)
    assert first == second
    assert verify_event_integrity(recorded_hash=first, **kwargs)
    assert not verify_event_integrity(
        recorded_hash=first,
        **{**kwargs, "payload": {"request_id": "request-1", "value": 8}},
    )


def test_event_integrity_hash_detects_metadata_tampering():
    from kernel.durability import event_integrity_hash, verify_event_integrity

    kwargs = {
        "event_id": "event-2",
        "event_type": "test.event",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "payload": {"request_id": "request-2"},
        "request_id": "request-2",
        "provenance": {"source": "test"},
    }
    recorded = event_integrity_hash(**kwargs)
    assert not verify_event_integrity(
        recorded_hash=recorded,
        **{**kwargs, "event_type": "test.changed"},
    )


def test_sqlite_event_integrity_verification_detects_tampering():
    store = SQLiteEventStore()
    try:
        sequence = store.append(
            event_id="event-integrity",
            event_type="test.event",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={"request_id": "request-integrity", "value": 1},
            request_id="request-integrity",
            provenance={"source": "test"},
        )
        assert store.verify_event_integrity(sequence) is True
        store._connection.execute(
            "UPDATE events SET payload=? WHERE sequence=?",
            ('{"request_id":"request-integrity","value":2}', sequence),
        )
        store._connection.commit()
        assert store.verify_event_integrity(sequence) is False
    finally:
        store.close()
