"""Core domain objects for the first Kernel vertical slice."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Principal:
    id: UUID
    kind: str
    authenticated: bool = True


@dataclass(frozen=True)
class Request:
    id: UUID
    principal_id: UUID
    operation: str
    resource: str
    parameters: Mapping[str, Any]
    received_at: datetime
    idempotency_key: str


@dataclass(frozen=True)
class Proposal:
    id: UUID
    request_id: UUID
    principal_id: UUID
    operation: str
    resource: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True)
class Context:
    id: UUID
    principal_id: UUID
    resource: str
    captured_at: datetime


@dataclass(frozen=True)
class GovernanceDecision:
    decision: str
    proposal_id: UUID
    policy_version: str
    reason: str


@dataclass(frozen=True)
class Authorization:
    id: UUID
    principal_id: UUID
    proposal_id: UUID
    operation: str
    resource: str
    issued_at: datetime
    expires_at: datetime

    def valid_at(self, at: datetime) -> bool:
        return self.expires_at > at


@dataclass(frozen=True)
class Outcome:
    attempt_id: UUID
    status: str
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class Event:
    """Evidence record with explicit lineage metadata."""

    id: UUID
    sequence: int
    event_type: str
    timestamp: datetime
    payload: Mapping[str, Any]
    schema_version: int = 1
    principal_id: UUID | None = None
    request_id: UUID | None = None
    causation_id: UUID | None = None
    correlation_id: UUID | None = None
    provenance: Mapping[str, Any] = field(default_factory=dict)


def new_id() -> UUID:
    return uuid4()
