"""Deterministic cryptographic integrity for protected Kernel event evidence."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

from .json import canonical_json

AUDIT_HASH_ALGORITHM = "sha256"
AUDIT_HASH_VERSION = 1


def event_integrity_hash(
    *,
    event_id: str,
    event_type: str,
    timestamp: str,
    payload: Mapping[str, Any],
    schema_version: int = 1,
    principal_id: str | None = None,
    request_id: str | None = None,
    causation_id: str | None = None,
    correlation_id: str | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> str:
    """Hash the canonical protected event representation."""
    protected = {
        "algorithm": AUDIT_HASH_ALGORITHM,
        "hash_version": AUDIT_HASH_VERSION,
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "payload": payload,
        "schema_version": schema_version,
        "principal_id": principal_id,
        "request_id": request_id,
        "causation_id": causation_id,
        "correlation_id": correlation_id,
        "provenance": provenance or {},
    }
    return hashlib.sha256(canonical_json(protected).encode("utf-8")).hexdigest()


def verify_event_integrity(
    *,
    recorded_hash: str,
    event_id: str,
    event_type: str,
    timestamp: str,
    payload: Mapping[str, Any],
    schema_version: int = 1,
    principal_id: str | None = None,
    request_id: str | None = None,
    causation_id: str | None = None,
    correlation_id: str | None = None,
    provenance: Mapping[str, Any] | None = None,
) -> bool:
    """Return whether a recorded event hash matches its protected representation."""
    expected = event_integrity_hash(
        event_id=event_id,
        event_type=event_type,
        timestamp=timestamp,
        payload=payload,
        schema_version=schema_version,
        principal_id=principal_id,
        request_id=request_id,
        causation_id=causation_id,
        correlation_id=correlation_id,
        provenance=provenance,
    )
    return hashlib.sha256(recorded_hash.encode("ascii")).digest() == hashlib.sha256(
        expected.encode("ascii")
    ).digest()
