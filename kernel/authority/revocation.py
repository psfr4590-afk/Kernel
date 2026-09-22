"""Authorization revocation primitives."""

from __future__ import annotations

from typing import Any, Mapping, Protocol
from uuid import UUID


class RevocationStore(Protocol):
    def revoke_authorization(self, authorization_id: str, revoked_at: str, reason: str, *,
                             event_id: str, principal_id: str | None = None,
                             request_id: str | None = None, correlation_id: str | None = None,
                             provenance: Mapping[str, Any] | None = None) -> int: ...

    def is_authorization_revoked(self, authorization_id: str) -> bool: ...


class RevocationRegistry:
    """Process-local revocation registry for the initial execution slice."""

    def __init__(self) -> None:
        self._revoked: set[UUID] = set()

    def revoke(self, authorization_id: UUID) -> None:
        self._revoked.add(authorization_id)

    def is_revoked(self, authorization_id: UUID) -> bool:
        return authorization_id in self._revoked


class SQLiteRevocationRegistry:
    """Durable revocation registry backed by SQLite."""

    def __init__(self, store: RevocationStore) -> None:
        self._store = store

    def revoke(self, authorization_id: UUID, revoked_at: str, reason: str, *,
               event_id: UUID, principal_id: UUID | None = None,
               request_id: UUID | None = None, correlation_id: UUID | None = None,
               provenance: Mapping[str, Any] | None = None) -> int:
        return self._store.revoke_authorization(
            str(authorization_id), revoked_at, reason, event_id=str(event_id),
            principal_id=None if principal_id is None else str(principal_id),
            request_id=None if request_id is None else str(request_id),
            correlation_id=None if correlation_id is None else str(correlation_id),
            provenance=provenance,
        )

    def is_revoked(self, authorization_id: UUID) -> bool:
        return self._store.is_authorization_revoked(str(authorization_id))
