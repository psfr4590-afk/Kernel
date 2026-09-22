"""Deterministic reconstruction of request state from authoritative events."""

from __future__ import annotations

import json
from typing import Any


def replay_request_state(events: list[tuple[int, str, str, str, str]], request_id: str) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for sequence, _event_id, event_type, _timestamp, payload in events:
        data = json.loads(payload)
        if data.get("request_id") != request_id:
            continue
        if event_type == "request.denied":
            state = {"status": "DENIED", "event_sequence": sequence}
        elif event_type.startswith("execution."):
            state = {
                "status": data["outcome"],
                "event_sequence": sequence,
                "attempt_id": data.get("attempt_id"),
            }
    return state
