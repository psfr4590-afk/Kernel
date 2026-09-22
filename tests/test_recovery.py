from kernel.durability import SQLiteEventStore, assess_request_recovery


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
