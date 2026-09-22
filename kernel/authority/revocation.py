"""Durable revocation state used by authorization enforcement."""

from __future__ import annotations

from uuid import UUID


class RevocationRegistry:
    def __init__(self) -> None:
        self._revoked: set[UUID] = set()

    def revoke(self, authorization_id: UUID) -> None:
        self._revoked.add(authorization_id)

    def is_revoked(self, authorization_id: UUID) -> bool:
        return authorization_id in self._revoked
