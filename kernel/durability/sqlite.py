"""Minimal authoritative SQLite event and state store."""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Mapping

from .json import canonical_json


class StateSequenceError(ValueError):
    """Raised when state would move backwards or be written twice at one sequence."""


class AuthorizationIssuanceError(ValueError):
    """Raised when durable authorization issuance conflicts with prior evidence."""


class SQLiteEventStore:
    """Append immutable events and materialize derived state transactionally."""

    def __init__(self, database: str = ":memory:") -> None:
        self._connection = sqlite3.connect(database)
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                schema_version INTEGER NOT NULL DEFAULT 1,
                principal_id TEXT,
                request_id TEXT,
                causation_id TEXT,
                correlation_id TEXT,
                provenance TEXT NOT NULL DEFAULT '{}',
                integrity_hash TEXT
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS revocations (
                authorization_id TEXT PRIMARY KEY,
                revoked_at TEXT NOT NULL,
                reason TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS authorizations (
                authorization_id TEXT PRIMARY KEY,
                principal_id TEXT NOT NULL,
                proposal_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                resource TEXT NOT NULL,
                issued_at TEXT NOT NULL,
                expires_at TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS state (
                subject TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                event_sequence INTEGER NOT NULL
            )
            """
        )
        self._ensure_integrity_hash_column()
        self._connection.commit()

    def _ensure_integrity_hash_column(self) -> None:
        columns = {row[1] for row in self._connection.execute("PRAGMA table_info(events)").fetchall()}
        if "integrity_hash" not in columns:
            self._connection.execute("ALTER TABLE events ADD COLUMN integrity_hash TEXT")

    def save_authorization(self, authorization: Any) -> None:
        """Persist an issued authorization record idempotently."""
        try:
            self._connection.execute(
                """
                INSERT INTO authorizations(
                    authorization_id,principal_id,proposal_id,operation,
                    resource,issued_at,expires_at
                ) VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(authorization_id) DO NOTHING
                """,
                (
                    str(authorization.id),
                    str(authorization.principal_id),
                    str(authorization.proposal_id),
                    authorization.operation,
                    authorization.resource,
                    authorization.issued_at.isoformat(),
                    authorization.expires_at.isoformat(),
                ),
            )
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

    def append_authorization_issued(
        self,
        authorization: Any,
        *,
        event_id: str,
        timestamp: str,
        request_id: str,
        correlation_id: str | None,
        provenance: Mapping[str, Any] | None = None,
    ) -> int:
        """Persist an authorization and its issuance evidence atomically and idempotently."""
        payload = {
            "authorization_id": str(authorization.id),
            "proposal_id": str(authorization.proposal_id),
            "principal_id": str(authorization.principal_id),
            "request_id": request_id,
            "operation": authorization.operation,
            "resource": authorization.resource,
            "issued_at": authorization.issued_at.isoformat(),
            "expires_at": authorization.expires_at.isoformat(),
        }
        event_data = canonical_json(payload)
        provenance_data = canonical_json(provenance or {})
        authorization_id = str(authorization.id)
        try:
            existing = self._connection.execute(
                """
                SELECT principal_id,proposal_id,operation,resource,issued_at,expires_at
                FROM authorizations WHERE authorization_id=?
                """,
                (authorization_id,),
            ).fetchone()
            expected_record = (
                str(authorization.principal_id),
                str(authorization.proposal_id),
                authorization.operation,
                authorization.resource,
                authorization.issued_at.isoformat(),
                authorization.expires_at.isoformat(),
            )
            if existing is not None and tuple(existing) != expected_record:
                raise AuthorizationIssuanceError(
                    "authorization id already exists with conflicting authority"
                )

            self._connection.execute(
                """
                INSERT INTO authorizations(
                    authorization_id,principal_id,proposal_id,operation,
                    resource,issued_at,expires_at
                ) VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(authorization_id) DO NOTHING
                """,
                (
                    authorization_id,
                    str(authorization.principal_id),
                    str(authorization.proposal_id),
                    authorization.operation,
                    authorization.resource,
                    authorization.issued_at.isoformat(),
                    authorization.expires_at.isoformat(),
                ),
            )

            issuance_rows = self._connection.execute(
                """
                SELECT sequence,event_id,timestamp,payload,schema_version,
                       principal_id,request_id,correlation_id,provenance
                FROM events
                WHERE event_type='authorization.issued'
                ORDER BY sequence
                """
            ).fetchall()
            for row in issuance_rows:
                try:
                    recorded_payload = json.loads(row[3])
                except (TypeError, json.JSONDecodeError) as exc:
                    raise AuthorizationIssuanceError(
                        "existing authorization issuance evidence is not valid JSON"
                    ) from exc
                if recorded_payload.get("authorization_id") != authorization_id:
                    continue
                if (
                    recorded_payload != payload
                    or row[4] != 1
                    or row[5] != str(authorization.principal_id)
                    or row[6] != request_id
                    or row[7] != correlation_id
                    or row[8] != provenance_data
                ):
                    raise AuthorizationIssuanceError(
                        "authorization id already has conflicting issuance evidence"
                    )
                self._connection.commit()
                return int(row[0])

            cursor = self._connection.execute(
                """
                INSERT INTO events(
                    event_id,event_type,timestamp,payload,schema_version,
                    principal_id,request_id,correlation_id,provenance
                ) VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    event_id,
                    "authorization.issued",
                    timestamp,
                    event_data,
                    1,
                    str(authorization.principal_id),
                    request_id,
                    correlation_id,
                    provenance_data,
                ),
            )
            self._connection.commit()
            return int(cursor.lastrowid)
        except Exception:
            self._connection.rollback()
            raise

    def get_authorization(self, authorization_id: str) -> Mapping[str, Any] | None:
        row = self._connection.execute(
            """
            SELECT authorization_id,principal_id,proposal_id,operation,
                   resource,issued_at,expires_at
            FROM authorizations WHERE authorization_id=?
            """,
            (authorization_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "principal_id": row[1],
            "proposal_id": row[2],
            "operation": row[3],
            "resource": row[4],
            "issued_at": row[5],
            "expires_at": row[6],
        }

    def append(
        self,
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
    ) -> int:
        data = canonical_json(payload)
        provenance_data = canonical_json(provenance or {})
        cursor = self._connection.execute(
            """
            INSERT INTO events(
                event_id,event_type,timestamp,payload,schema_version,
                principal_id,request_id,causation_id,correlation_id,provenance
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                event_id,
                event_type,
                timestamp,
                data,
                schema_version,
                principal_id,
                request_id,
                causation_id,
                correlation_id,
                provenance_data,
            ),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def append_with_state(
        self,
        *,
        event_id: str,
        event_type: str,
        timestamp: str,
        payload: Mapping[str, Any],
        subject: str,
        state: Mapping[str, Any],
        schema_version: int = 1,
        principal_id: str | None = None,
        request_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
        provenance: Mapping[str, Any] | None = None,
    ) -> int:
        """Commit the event and its derived state together, or neither."""
        event_data = canonical_json(payload)
        state_data = canonical_json(state)
        provenance_data = canonical_json(provenance or {})
        try:
            cursor = self._connection.execute(
                """
                INSERT INTO events(
                    event_id,event_type,timestamp,payload,schema_version,
                    principal_id,request_id,causation_id,correlation_id,provenance
                ) VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    event_id,
                    event_type,
                    timestamp,
                    event_data,
                    schema_version,
                    principal_id,
                    request_id,
                    causation_id,
                    correlation_id,
                    provenance_data,
                ),
            )
            sequence = int(cursor.lastrowid)
            existing = self._connection.execute(
                "SELECT event_sequence FROM state WHERE subject=?",
                (subject,),
            ).fetchone()
            if existing is not None and sequence <= int(existing[0]):
                raise StateSequenceError("state event sequence must increase monotonically")
            self._connection.execute(
                """
                INSERT INTO state(subject,state_json,event_sequence)
                VALUES(?,?,?)
                ON CONFLICT(subject) DO UPDATE SET
                    state_json=excluded.state_json,
                    event_sequence=excluded.event_sequence
                """,
                (subject, state_data, sequence),
            )
            self._connection.commit()
            return sequence
        except Exception:
            self._connection.rollback()
            raise

    def rematerialize_state(
        self,
        *,
        subject: str,
        state: Mapping[str, Any],
        event_sequence: int,
    ) -> None:
        """Replace derived state from authoritative history without creating an event."""
        if event_sequence <= 0:
            raise ValueError("event_sequence must be positive")
        state_data = canonical_json(state)
        try:
            exists = self._connection.execute(
                "SELECT 1 FROM events WHERE sequence=?",
                (event_sequence,),
            ).fetchone()
            if exists is None:
                raise ValueError("event_sequence does not exist in authoritative history")
            self._connection.execute(
                """
                INSERT INTO state(subject,state_json,event_sequence)
                VALUES(?,?,?)
                ON CONFLICT(subject) DO UPDATE SET
                    state_json=excluded.state_json,
                    event_sequence=excluded.event_sequence
                """,
                (subject, state_data, event_sequence),
            )
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

    def all_events(self) -> list[tuple[int, str, str, str, str]]:
        rows = self._connection.execute(
            "SELECT sequence,event_id,event_type,timestamp,payload "
            "FROM events ORDER BY sequence"
        ).fetchall()
        return [(int(a), str(b), str(c), str(d), str(e)) for a, b, c, d, e in rows]

    def get_state(self, subject: str) -> tuple[str, int] | None:
        row = self._connection.execute(
            "SELECT state_json,event_sequence FROM state WHERE subject=?",
            (subject,),
        ).fetchone()
        return None if row is None else (str(row[0]), int(row[1]))

    def revoke_authorization(
        self,
        authorization_id: str,
        revoked_at: str,
        reason: str,
        *,
        event_id: str,
        principal_id: str | None = None,
        request_id: str | None = None,
        correlation_id: str | None = None,
        provenance: Mapping[str, Any] | None = None,
    ) -> int:
        """Durably revoke authority and record revocation evidence atomically."""
        event_data = canonical_json({
            "authorization_id": authorization_id,
            "reason": reason,
            "request_id": request_id,
        })
        provenance_data = canonical_json(provenance or {})
        try:
            self._connection.execute(
                "INSERT INTO revocations(authorization_id,revoked_at,reason) VALUES(?,?,?)",
                (authorization_id, revoked_at, reason),
            )
            cursor = self._connection.execute(
                """
                INSERT INTO events(
                    event_id,event_type,timestamp,payload,schema_version,
                    principal_id,request_id,correlation_id,provenance
                ) VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (event_id, "authorization.revoked", revoked_at, event_data, 1,
                 principal_id, request_id, correlation_id, provenance_data),
            )
            self._connection.commit()
            return int(cursor.lastrowid)
        except Exception:
            self._connection.rollback()
            raise

    def is_authorization_revoked(self, authorization_id: str) -> bool:
        row = self._connection.execute(
            "SELECT 1 FROM revocations WHERE authorization_id=?",
            (authorization_id,),
        ).fetchone()
        return row is not None

    def close(self) -> None:
        self._connection.close()
