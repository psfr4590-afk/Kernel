"""Durability and evidence boundaries."""

from .audit import AUDIT_HASH_ALGORITHM, AUDIT_HASH_VERSION, event_integrity_hash, verify_event_integrity

from .json import CanonicalJSONError, canonical_json
from .recovery import (
    RecoveryAssessment,
    assess_request_recovery,
    record_interruption,
    record_unknown_recovery,
    rematerialize_request_state,
)
from .replay import replay_request_state
from .sqlite import AuthorizationIssuanceError, SQLiteEventStore, StateSequenceError

__all__ = [
    "AUDIT_HASH_ALGORITHM",
    "AUDIT_HASH_VERSION",
    "AuthorizationIssuanceError",
    "event_integrity_hash",
    "CanonicalJSONError",
    "RecoveryAssessment",
    "SQLiteEventStore",
    "StateSequenceError",
    "assess_request_recovery",
    "verify_event_integrity",
    "canonical_json",
    "replay_request_state",
    "record_unknown_recovery",
    "record_interruption",
    "rematerialize_request_state",
]
