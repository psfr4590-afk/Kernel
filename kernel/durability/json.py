"""Canonical JSON representation required by ADR-003."""

from __future__ import annotations

import json
from typing import Any


class CanonicalJSONError(ValueError):
    """Raised when data cannot be represented as canonical Kernel JSON."""


def canonical_json(value: Any) -> str:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise CanonicalJSONError("value is not valid canonical JSON") from exc
    return encoded
