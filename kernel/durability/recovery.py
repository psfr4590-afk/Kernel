"""Evidence-first recovery primitives."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from uuid import NAMESPACE_URL, uuid5

from .replay import replay_request_state
from .sqlite import SQLiteEventStore


EventRow = Sequence[Any]


def _event_request_id(event: EventRow) -> str | None:
    """Read request identity from potentially corrupted event payload safely."""
    try:
        payload = json.loads(event[4])
    except (TypeError, ValueError):
        return None
    return payload.get("request_id") if isinstance(payload, dict) else None


@dataclass(frozen=True)
class RecoveryAssessment:
    request_id: str
    status: str
    state: Mapping[str, Any]
    evidence_count: int
    requires_reconciliation: bool
    reason: str


def assess_request_recovery(
    events: list[EventRow],
    request_id: str,
) -> RecoveryAssessment:
    """Assess local evidence without retrying, renewing, or creating an effect."""
    matching: list[EventRow] = []
    for event in events:
        try:
            payload = json.loads(event[4])
        except (TypeError, ValueError):
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("request_id") == request_id:
            matching.append(event)

    state = replay_request_state(matching, request_id)
    if not state:
        return RecoveryAssessment(
            request_id=request_id,
            status="UNKNOWN",
            state={},
            evidence_count=len(matching),
            requires_reconciliation=True,
            reason="no authoritative terminal outcome was reconstructed",
        )

    status = str(state["status"])
    if status in {"SUCCEEDED", "FAILED", "PARTIAL", "DENIED", "BLOCKED"}:
        return RecoveryAssessment(
            request_id=request_id,
            status=status,
            state=state,
            evidence_count=len(matching),
            requires_reconciliation=False,
            reason="terminal status reconstructed from durable event history",
        )

    return RecoveryAssessment(
        request_id=request_id,
        status="UNKNOWN",
        state=state,
        evidence_count=len(matching),
        requires_reconciliation=True,
        reason="evidence does not establish a terminal effect status",
    )


def rematerialize_request_state(
    store: SQLiteEventStore,
    request_id: str,
) -> RecoveryAssessment:
    """Rebuild derived request state from immutable event history."""
    assessment = assess_request_recovery(store.verified_events(), request_id)
    if not assessment.state:
        return assessment
    event_sequence = assessment.state.get("event_sequence")
    if not isinstance(event_sequence, int):
        return assessment
    store.rematerialize_state(
        subject=request_id,
        state=assessment.state,
        event_sequence=event_sequence,
    )
    return assess_request_recovery(store.verified_events(), request_id)


def record_unknown_recovery(
    store: SQLiteEventStore,
    request_id: str,
    *,
    reason: str,
    timestamp: str,
    principal_id: str | None = None,
    correlation_id: str | None = None,
) -> RecoveryAssessment:
    """Durably record unresolved recovery as UNKNOWN without creating an effect.

    The recovery evidence identifier is deterministic for the request, making
    repeated recovery assessment idempotent at the evidence boundary.
    """
    try:
        store._connection.execute("BEGIN IMMEDIATE")
        assessment = assess_request_recovery(store.all_events(), request_id)
        if assessment.status != "UNKNOWN":
            store._connection.commit()
            return assessment

        existing_unknown = any(
            row[2] == "recovery.unknown"
            and _event_request_id(row) == request_id
            for row in store.all_events()
        )
        if not existing_unknown:
            event_id = uuid5(NAMESPACE_URL, f"kernel:recovery:unknown:{request_id}")
            store.append_with_state(
                event_id=str(event_id),
                event_type="recovery.unknown",
                timestamp=timestamp,
                payload={
                    "request_id": request_id,
                    "status": "UNKNOWN",
                    "reason": reason,
                },
                subject=request_id,
                state={"status": "UNKNOWN"},
                principal_id=principal_id,
                request_id=request_id,
                correlation_id=correlation_id or request_id,
                provenance={"source": "kernel.recovery"},
            )
        else:
            store._connection.commit()
        return assess_request_recovery(store.all_events(), request_id)
    except Exception:
        store._connection.rollback()
        raise


def record_interruption(
    store: SQLiteEventStore,
    request_id: str,
    *,
    timestamp: str,
    reason: str,
    principal_id: str | None = None,
    correlation_id: str | None = None,
) -> RecoveryAssessment:
    """Record an interruption boundary without claiming an execution outcome."""
    try:
        store._connection.execute("BEGIN IMMEDIATE")
        assessment = assess_request_recovery(store.all_events(), request_id)
        if assessment.status in {"SUCCEEDED", "FAILED", "PARTIAL", "DENIED", "BLOCKED"}:
            store._connection.commit()
            return assessment

        existing = any(
            row[2] == "recovery.interrupted"
            and _event_request_id(row) == request_id
            for row in store.all_events()
        )
        if not existing:
            event_id = uuid5(NAMESPACE_URL, f"kernel:recovery:interrupted:{request_id}")
            store.append(
                event_id=str(event_id),
                event_type="recovery.interrupted",
                timestamp=timestamp,
                payload={
                    "request_id": request_id,
                    "status": "INTERRUPTED",
                    "reason": reason,
                },
                principal_id=principal_id,
                request_id=request_id,
                correlation_id=correlation_id or request_id,
                provenance={"source": "kernel.recovery"},
            )
        else:
            store._connection.commit()

        return assess_request_recovery(store.all_events(), request_id)
    except Exception:
        store._connection.rollback()
        raise
