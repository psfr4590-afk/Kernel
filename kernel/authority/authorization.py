"""Durable authorization record primitives."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Protocol
from uuid import UUID

from kernel.models import Authorization


class AuthorizationStore(Protocol):
    def save_authorization(self, authorization: Authorization) -> None: ...

    def get_authorization(self, authorization_id: str) -> Mapping[str, Any] | None: ...


class SQLiteAuthorizationStore:
    """Durably persist issued authorization records without granting authority."""

    def __init__(self, store: AuthorizationStore) -> None:
        self._store = store

    def save(self, authorization: Authorization) -> None:
        self._store.save_authorization(authorization)

    def get(self, authorization_id: UUID) -> Authorization | None:
        record = self._store.get_authorization(str(authorization_id))
        if record is None:
            return None
        return Authorization(
            id=UUID(str(record["id"])),
            principal_id=UUID(str(record["principal_id"])),
            proposal_id=UUID(str(record["proposal_id"])),
            operation=str(record["operation"]),
            resource=str(record["resource"]),
            issued_at=datetime.fromisoformat(str(record["issued_at"])),
            expires_at=datetime.fromisoformat(str(record["expires_at"])),
        )
