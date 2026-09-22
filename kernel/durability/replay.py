"""Deterministic reconstruction of request state from authoritative events."""

from __future__ import annotations

import json
from typing import Any, Sequence


EventRow = Sequence[Any]

TERMINAL_EXECUTION_EVENTS = frozenset({
    "execution.succeeded",
    "execution.failed",
    "execution.partial",
    "execution.blocked",
})


def replay_request_state(events: list[EventRow], request_id: str) -> dict[str, Any]:
    """Reconstruct the latest known request state without creating effects."""
    state: dict[str, Any] = {}
    for sequence, _event_id, event_type, _timestamp, payload, *_metadata in events:
        data = json.loads(payload)
        if data.get("request_id") != request_id:
            continue
        if event_type == "request.denied":
            state = {"status": "DENIED", "event_sequence": sequence}
        elif event_type == "recovery.unknown":
            state = {
                "status": "UNKNOWN",
                "event_sequence": sequence,
                "recovery": True,
            }
        elif event_type in TERMINAL_EXECUTION_EVENTS and "outcome" in data:
            state = {
                "status": data["outcome"],
                "event_sequence": sequence,
                "attempt_id": data.get("attempt_id"),
            }
    return state
