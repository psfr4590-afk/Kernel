"""Minimal authoritative SQLite event and state store."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any, Mapping

from .audit import event_integrity_hash, verify_event_integrity
from .json import canonical_json


class StateSequenceError(ValueError):
    """Raised when state would move backwards or be written twice at one sequence."""


class AuthorizationIssuanceError(ValueError):
    """Raised when durable authorization issuance conflicts with prior evidence."""


class IdempotencyConflictError(ValueError):
    """Raised when an idempotency key is reused for a different operation."""


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
            CREATE TABLE IF NOT EXISTS operations (
                principal_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                request_id TEXT NOT NULL UNIQUE,
                operation TEXT NOT NULL,
                resource TEXT NOT NULL,
                request_fingerprint TEXT NOT NULL,
                claimed_sequence INTEGER NOT NULL,
                PRIMARY KEY(principal_id, idempotency_key)
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

    def _store_event_integrity_hash(self, sequence: int, *, event_id: str, event_type: str, timestamp: str, payload: Mapping[str, Any], schema_version: int, principal_id: str | None, request_id: str | None, causation_id: str | None, correlation_id: str | None, provenance: Mapping[str, Any] | None) -> None:
        integrity_hash = event_integrity_hash(
            event_id=event_id,
            event_type=event_type,
            timestamp=timestamp,
            payload=payload,
            schema_version=schema_version,
            principal_id=principal_id,
            request_id=request_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
            provenance=provenance or {},
        )
        self._connection.execute(
            "UPDATE events SET integrity_hash=? WHERE sequence=?",
            (integrity_hash, sequence),
        )
    def claim_operation(
        self,
        *,
        principal_id: str,
        idempotency_key: str,
        request_id: str,
        operation: str,
        resource: str,
        parameters: Mapping[str, Any],
        timestamp: str,
        correlation_id: str | None,
        provenance: Mapping[str, Any] | None = None,
    ) -> tuple[str, int, bool]:
        """Durably claim an operation identity before governance or execution."""
        if not idempotency_key:
            raise ValueError("idempotency_key is required")
        fingerprint_data = {
            "principal_id": principal_id,
            "operation": operation,
            "resource": resource,
            "parameters": parameters,
        }
        fingerprint = hashlib.sha256(
            canonical_json(fingerprint_data).encode("utf-8")
        ).hexdigest()
        payload = {
            "request_id": request_id,
            "principal_id": principal_id,
            "idempotency_key": idempotency_key,
            "operation": operation,
            "resource": resource,
            "request_fingerprint": fingerprint,
        }
        provenance_data = provenance or {}
        try:
            existing = self._connection.execute(
                """
                SELECT request_id,operation,resource,request_fingerprint,claimed_sequence
                FROM operations WHERE principal_id=? AND idempotency_key=?
                """,
                (principal_id, idempotency_key),
            ).fetchone()
            if existing is not None:
                if (
                    existing[1] != operation
                    or existing[2] != resource
                    or existing[3] != fingerprint
                ):
                    raise IdempotencyConflictError(
                        "idempotency key already identifies a different operation"
                    )
                return str(existing[0]), int(existing[4]), False

            event_id = str(__import__("uuid").uuid4())
            cursor = self._connection.execute(
                """
                INSERT INTO events(
                    event_id,event_type,timestamp,payload,schema_version,
                    principal_id,request_id,correlation_id,provenance
                ) VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    event_id,
                    "operation.claimed",
                    timestamp,
                    canonical_json(payload),
                    1,
                    principal_id,
                    request_id,
                    correlation_id,
                    canonical_json(provenance_data),
                ),
            )
            sequence = int(cursor.lastrowid)
            self._store_event_integrity_hash(
                sequence,
                event_id=event_id,
                event_type="operation.claimed",
                timestamp=timestamp,
                payload=payload,
                schema_version=1,
                principal_id=principal_id,
                request_id=request_id,
                causation_id=None,
                correlation_id=correlation_id,
                provenance=provenance_data,
            )
            self._connection.execute(
                """
                INSERT INTO operations(
                    principal_id,idempotency_key,request_id,operation,resource,
                    request_fingerprint,claimed_sequence
                ) VALUES(?,?,?,?,?,?,?)
                """,
                (
                    principal_id,
                    idempotency_key,
                    request_id,
                    operation,
                    resource,
                    fingerprint,
                    sequence,
                ),
            )
            self._connection.commit()
            return request_id, sequence, True
        except Exception:
            self._connection.rollback()
            raise

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
            sequence = int(cursor.lastrowid)
            self._store_event_integrity_hash(
                sequence,
                event_id=event_id,
                event_type="authorization.issued",
                timestamp=timestamp,
                payload=payload,
                schema_version=1,
                principal_id=str(authorization.principal_id),
                request_id=request_id,
                causation_id=None,
                correlation_id=correlation_id,
                provenance=provenance or {},
            )
            self._connection.commit()
            return sequence
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
        sequence = int(cursor.lastrowid)
        self._store_event_integrity_hash(
            sequence,
            event_id=event_id,
            event_type=event_type,
            timestamp=timestamp,
            payload=payload,
            schema_version=schema_version,
            principal_id=principal_id,
            request_id=request_id,
            causation_id=causation_id,
            correlation_id=correlation_id,
            provenance=provenance or {},
        )
        self._connection.commit()
        return sequence

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
            self._store_event_integrity_hash(
                sequence,
                event_id=event_id,
                event_type=event_type,
                timestamp=timestamp,
                payload=payload,
                schema_version=schema_version,
                principal_id=principal_id,
                request_id=request_id,
                causation_id=causation_id,
                correlation_id=correlation_id,
                provenance=provenance or {},
            )
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
            sequence = int(cursor.lastrowid)
            self._store_event_integrity_hash(
                sequence,
                event_id=event_id,
                event_type="authorization.revoked",
                timestamp=revoked_at,
                payload={
                    "authorization_id": authorization_id,
                    "reason": reason,
                    "request_id": request_id,
                },
                schema_version=1,
                principal_id=principal_id,
                request_id=request_id,
                causation_id=None,
                correlation_id=correlation_id,
                provenance=provenance or {},
            )
            self._connection.commit()
            return sequence
        except Exception:
            self._connection.rollback()
            raise

    def verify_event_integrity(self, sequence: int) -> bool:
        row = self._connection.execute(
            "SELECT event_id,event_type,timestamp,payload,schema_version,principal_id,request_id,causation_id,correlation_id,provenance,integrity_hash FROM events WHERE sequence=?",
            (sequence,),
        ).fetchone()
        if row is None or row[10] is None:
            return False
        try:
            payload = json.loads(row[3])
            provenance = json.loads(row[9])
        except (TypeError, json.JSONDecodeError):
            return False
        return verify_event_integrity(
            recorded_hash=str(row[10]),
            event_id=str(row[0]),
            event_type=str(row[1]),
            timestamp=str(row[2]),
            payload=payload,
            schema_version=int(row[4]),
            principal_id=row[5],
            request_id=row[6],
            causation_id=row[7],
            correlation_id=row[8],
            provenance=provenance,
        )

    def is_authorization_revoked(self, authorization_id: str) -> bool:
        row = self._connection.execute(
            "SELECT 1 FROM revocations WHERE authorization_id=?",
            (authorization_id,),
        ).fetchone()
        return row is not None

    def close(self) -> None:
        self._connection.close()
