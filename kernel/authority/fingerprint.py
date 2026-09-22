"""Canonical fingerprints for authorization-bound consequential parameters."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

from kernel.durability.json import canonical_json


def parameters_fingerprint(parameters: Mapping[str, Any]) -> str:
    """Return a deterministic SHA-256 fingerprint of authorized parameters."""
    return hashlib.sha256(
        canonical_json(dict(parameters)).encode("utf-8")
    ).hexdigest()
