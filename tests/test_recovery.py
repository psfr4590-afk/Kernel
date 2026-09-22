import pytest

from kernel.durability import (
    SQLiteEventStore,
    assess_request_recovery,
    record_interruption,
    record_unknown_recovery,
    rematerialize_request_state,
)


def test_recovery_reconstructs_terminal_denial_without_new_effect() -> None:
    store = SQLiteEventStore()
    try:
        store.append(
            event_id="event-1",
            event_type="request.denied",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={"request_id": "request-1", "reason": "policy"},
        )
        assessment = assess_request_recovery(store.all_events(), "request-1")
        assert assessment.status == "DENIED"
        assert assessment.requires_reconciliation is False
        assert assessment.evidence_count == 1
    finally:
        store.close()


def test_recovery_reports_unknown_when_effect_status_is_not_established() -> None:
    store = SQLiteEventStore()
    try:
        store.append(
            event_id="event-1",
            event_type="execution.attempted",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={"request_id": "request-1", "attempt_id": "attempt-1"},
        )
        assessment = assess_request_recovery(store.all_events(), "request-1")
        assert assessment.status == "UNKNOWN"
        assert assessment.requires_reconciliation is True
        assert assessment.evidence_count == 1
    finally:
        store.close()


def test_unknown_recovery_is_durable_and_idempotent() -> None:
    store = SQLiteEventStore()
    try:
        first = record_unknown_recovery(
            store,
            "request-1",
            reason="process interruption left invocation outcome uncertain",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        second = record_unknown_recovery(
            store,
            "request-1",
            reason="repeated recovery inspection",
            timestamp="2026-01-01T00:00:01+00:00",
        )

        assert first.status == "UNKNOWN"
        assert second.status == "UNKNOWN"
        assert second.requires_reconciliation is True
        recovery_events = [
            row for row in store.all_events() if row[2] == "recovery.unknown"
        ]
        assert len(recovery_events) == 1
        assert store.get_state("request-1") == ('{"status":"UNKNOWN"}', recovery_events[0][0])
    finally:
        store.close()


def test_recovery_does_not_override_later_terminal_evidence() -> None:
    store = SQLiteEventStore()
    try:
        store.append(
            event_id="event-1",
            event_type="execution.attempted",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={"request_id": "request-1", "attempt_id": "attempt-1"},
        )
        record_unknown_recovery(
            store,
            "request-1",
            reason="outcome uncertain",
            timestamp="2026-01-01T00:00:01+00:00",
        )
        store.append(
            event_id="event-2",
            event_type="execution.succeeded",
            timestamp="2026-01-01T00:00:02+00:00",
            payload={
                "request_id": "request-1",
                "attempt_id": "attempt-1",
                "outcome": "SUCCEEDED",
            },
        )
        assessment = assess_request_recovery(store.all_events(), "request-1")
        assert assessment.status == "SUCCEEDED"
        assert assessment.requires_reconciliation is False
    finally:
        store.close()


def test_interruption_evidence_is_idempotent_and_does_not_claim_success() -> None:
    store = SQLiteEventStore()
    try:
        from kernel.durability import record_interruption

        first = record_interruption(
            store,
            "request-2",
            timestamp="2026-01-01T00:00:00+00:00",
            reason="process stopped before outcome was recorded",
        )
        second = record_interruption(
            store,
            "request-2",
            timestamp="2026-01-01T00:00:01+00:00",
            reason="repeated interruption inspection",
        )
        assert first.status == "UNKNOWN"
        assert second.status == "UNKNOWN"
        assert second.requires_reconciliation is True
        events = [row for row in store.all_events() if row[2] == "recovery.interrupted"]
        assert len(events) == 1
    finally:
        store.close()


def test_interruption_does_not_override_existing_terminal_outcome() -> None:
    store = SQLiteEventStore()
    try:
        store.append(
            event_id="event-terminal",
            event_type="execution.succeeded",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={
                "request_id": "request-3",
                "attempt_id": "attempt-3",
                "outcome": "SUCCEEDED",
            },
        )
        assessment = record_interruption(
            store,
            "request-3",
            timestamp="2026-01-01T00:00:01+00:00",
            reason="late recovery inspection",
        )
        assert assessment.status == "SUCCEEDED"
        assert not [
            row for row in store.all_events()
            if row[2] == "recovery.interrupted"
        ]
    finally:
        store.close()


def test_recovery_rematerializes_derived_state_from_authoritative_history() -> None:
    store = SQLiteEventStore()
    try:
        request_id = "request-rematerialize"
        sequence = store.append(
            event_id="event-rematerialize",
            event_type="execution.succeeded",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={
                "request_id": request_id,
                "attempt_id": "attempt-1",
                "outcome": "SUCCEEDED",
            },
        )
        store._connection.execute(
            "INSERT INTO state(subject,state_json,event_sequence) VALUES(?,?,?)",
            (request_id, '{"status":"CORRUPTED"}', sequence),
        )
        store._connection.commit()

        assessment = rematerialize_request_state(store, request_id)

        assert assessment.status == "SUCCEEDED"
        assert store.get_state(request_id) == (
            '{"attempt_id":"attempt-1","event_sequence":1,"status":"SUCCEEDED"}',
            sequence,
        )
        assert len(store.all_events()) == 1
    finally:
        store.close()


def test_rematerialization_rejects_non_authoritative_sequence_without_mutation() -> None:
    store = SQLiteEventStore()
    try:
        request_id = "request-invalid-rematerialize"
        store.append(
            event_id="event-existing",
            event_type="request.denied",
            timestamp="2026-01-01T00:00:00+00:00",
            payload={"request_id": request_id},
        )
        before = store.get_state(request_id)
        with pytest.raises(ValueError):
            store.rematerialize_state(
                subject=request_id,
                state={"status": "DENIED"},
                event_sequence=999,
            )
        assert store.get_state(request_id) == before
    finally:
        store.close()
