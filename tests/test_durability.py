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
