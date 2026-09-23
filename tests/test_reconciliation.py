import threading

import pytest

from kernel.durability import (
    SQLiteEventStore,
    record_reconciliation,
    record_unknown_recovery,
)


def test_reconciliation_turns_unknown_into_evidenced_terminal_state() -> None:
    store = SQLiteEventStore()
    try:
        record_unknown_recovery(
            store,
            "request-1",
            reason="effect result was ambiguous",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        assessment = record_reconciliation(
            store,
            "request-1",
            status="SUCCEEDED",
            evidence={"remote_status": "committed", "operation_id": "remote-1"},
            source="remote-system",
            timestamp="2026-01-01T00:01:00+00:00",
        )
        assert assessment.status == "SUCCEEDED"
        assert assessment.requires_reconciliation is False
        events = store.all_events()
        assert [row[2] for row in events] == [
            "recovery.unknown",
            "recovery.reconciled",
        ]
    finally:
        store.close()


def test_reconciliation_is_idempotent_for_same_terminal_status() -> None:
    store = SQLiteEventStore()
    try:
        record_unknown_recovery(
            store,
            "request-2",
            reason="effect result was ambiguous",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        first = record_reconciliation(
            store,
            "request-2",
            status="FAILED",
            evidence={"remote_status": "rejected"},
            source="remote-system",
            timestamp="2026-01-01T00:01:00+00:00",
        )
        second = record_reconciliation(
            store,
            "request-2",
            status="FAILED",
            evidence={"remote_status": "rejected"},
            source="remote-system",
            timestamp="2026-01-01T00:02:00+00:00",
        )
        assert first.status == second.status == "FAILED"
        assert len([row for row in store.all_events() if row[2] == "recovery.reconciled"]) == 1
    finally:
        store.close()


def test_reconciliation_rejects_conflicting_terminal_evidence() -> None:
    store = SQLiteEventStore()
    try:
        record_unknown_recovery(
            store,
            "request-3",
            reason="effect result was ambiguous",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        record_reconciliation(
            store,
            "request-3",
            status="SUCCEEDED",
            evidence={"remote_status": "committed"},
            source="remote-system",
            timestamp="2026-01-01T00:01:00+00:00",
        )
        with pytest.raises(ValueError, match="conflicting authoritative outcome"):
            record_reconciliation(
                store,
                "request-3",
                status="FAILED",
                evidence={"remote_status": "rejected"},
                source="remote-system",
                timestamp="2026-01-01T00:02:00+00:00",
            )
        assert len(store.all_events()) == 2
    finally:
        store.close()


def test_reconciliation_requires_explicit_evidence_source_and_evidence() -> None:
    store = SQLiteEventStore()
    try:
        record_unknown_recovery(
            store,
            "request-4",
            reason="effect result was ambiguous",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        with pytest.raises(ValueError, match="source"):
            record_reconciliation(
                store,
                "request-4",
                status="SUCCEEDED",
                evidence={"remote_status": "committed"},
                source="",
                timestamp="2026-01-01T00:01:00+00:00",
            )
        with pytest.raises(ValueError, match="evidence"):
            record_reconciliation(
                store,
                "request-4",
                status="SUCCEEDED",
                evidence={},
                source="remote-system",
                timestamp="2026-01-01T00:01:00+00:00",
            )
        assert len(store.all_events()) == 1
    finally:
        store.close()



def test_reconciliation_is_concurrent_idempotent_across_store_connections(tmp_path) -> None:
    database = tmp_path / "kernel.db"
    setup = SQLiteEventStore(str(database))
    try:
        record_unknown_recovery(
            setup,
            "request-concurrent",
            reason="effect result was ambiguous",
            timestamp="2026-01-01T00:00:00+00:00",
        )
    finally:
        setup.close()

    stores = [SQLiteEventStore(str(database)), SQLiteEventStore(str(database))]
    barrier = threading.Barrier(2)
    results = []
    errors = []

    def reconcile(store: SQLiteEventStore) -> None:
        try:
            barrier.wait()
            results.append(
                record_reconciliation(
                    store,
                    "request-concurrent",
                    status="SUCCEEDED",
                    evidence={"remote_status": "committed"},
                    source="remote-system",
                    timestamp="2026-01-01T00:01:00+00:00",
                )
            )
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=reconcile, args=(store,)) for store in stores]
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors
        assert [result.status for result in results] == ["SUCCEEDED", "SUCCEEDED"]
        verification = SQLiteEventStore(str(database))
        try:
            events = [
                row for row in verification.all_events()
                if row[2] == "recovery.reconciled"
            ]
            assert len(events) == 1
            assert verification.get_state("request-concurrent") == (
                '{"status":"SUCCEEDED"}',
                events[0][0],
            )
        finally:
            verification.close()
    finally:
        for store in stores:
            store.close()
