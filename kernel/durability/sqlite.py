"""Minimal authoritative SQLite event and state store."""

from __future__ import annotations

import sqlite3
from typing import Any, Mapping

from .json import canonical_json


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
                payload TEXT NOT NULL
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
        self._connection.commit()

    def append(
        self,
        *,
        event_id: str,
        event_type: str,
        timestamp: str,
        payload: Mapping[str, Any],
    ) -> int:
        data = canonical_json(payload)
        cursor = self._connection.execute(
            "INSERT INTO events(event_id,event_type,timestamp,payload) VALUES(?,?,?,?)",
            (event_id, event_type, timestamp, data),
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
    ) -> int:
        """Commit the event and its derived state together, or neither."""
        event_data = canonical_json(payload)
        state_data = canonical_json(state)
        try:
            cursor = self._connection.execute(
                "INSERT INTO events(event_id,event_type,timestamp,payload) VALUES(?,?,?,?)",
                (event_id, event_type, timestamp, event_data),
            )
            sequence = int(cursor.lastrowid)
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

    def close(self) -> None:
        self._connection.close()
