"""Evidence-first recovery primitives."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from .replay import replay_request_state


@dataclass(frozen=True)
class RecoveryAssessment:
    request_id: str
    status: str
    state: Mapping[str, Any]
    evidence_count: int
    requires_reconciliation: bool
    reason: str


def assess_request_recovery(
    events: list[tuple[int, str, str, str, str]],
    request_id: str,
) -> RecoveryAssessment:
    """Assess recoverable local evidence without creating a new effect."""
    matching = []
    for event in events:
        try:
            payload = json.loads(event[4])
        except (TypeError, ValueError):
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
    if status in {"SUCCEEDED", "FAILED", "PARTIAL", "DENIED"}:
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
