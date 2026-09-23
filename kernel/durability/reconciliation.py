"""Explicit external-effect reconciliation evidence."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from .recovery import RecoveryAssessment, assess_request_recovery
from .sqlite import SQLiteEventStore

_RECONCILED_STATUSES = frozenset({"SUCCEEDED", "FAILED", "PARTIAL"})


def record_reconciliation(
    store: SQLiteEventStore,
    request_id: str,
    *,
    status: str,
    evidence: Mapping[str, Any],
    source: str,
    timestamp: str,
    principal_id: str | None = None,
    correlation_id: str | None = None,
) -> RecoveryAssessment:
    """Record an externally established terminal result without creating an effect.

    Reconciliation is evidence ingestion, not authorization. The operation must
    currently be unresolved, and the caller must identify the evidence source.
    Repeated identical reconciliation is idempotent through a deterministic
    evidence event identifier. Conflicting terminal evidence is rejected.
    """
    if status not in _RECONCILED_STATUSES:
        raise ValueError("reconciliation status must be SUCCEEDED, FAILED, or PARTIAL")
    if not source.strip():
        raise ValueError("reconciliation source is required")
    if not isinstance(evidence, Mapping) or not evidence:
        raise ValueError("reconciliation evidence must be a non-empty mapping")

    # Serialize the assess-and-record decision across SQLite connections. Without
    # this boundary, concurrent identical reconciliations can both observe
    # UNKNOWN and race to insert the same deterministic event identifier.
    try:
        store._connection.execute("BEGIN IMMEDIATE")
        assessment = assess_request_recovery(store.all_events(), request_id)
        if assessment.status != "UNKNOWN":
            store._connection.commit()
            if assessment.status != status:
                raise ValueError("request already has conflicting authoritative outcome")
            return assessment

        event_id = uuid5(NAMESPACE_URL, f"kernel:reconciliation:{request_id}:{status}")
        store.append_with_state(
            event_id=str(event_id),
            event_type="recovery.reconciled",
            timestamp=timestamp,
            payload={
                "request_id": request_id,
                "status": status,
                "outcome": status,
                "evidence": dict(evidence),
                "source": source,
            },
            subject=request_id,
            state={"status": status},
            principal_id=principal_id,
            request_id=request_id,
            correlation_id=correlation_id or request_id,
            provenance={
                "source": "kernel.recovery.reconciliation",
                "evidence_source": source,
            },
        )
        return assess_request_recovery(store.all_events(), request_id)
    except Exception:
        store._connection.rollback()
        raise
