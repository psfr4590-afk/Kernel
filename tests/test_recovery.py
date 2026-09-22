from kernel.durability import SQLiteEventStore, assess_request_recovery, record_unknown_recovery


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
