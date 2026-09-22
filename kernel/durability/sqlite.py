"""Minimal authoritative SQLite event store."""

from __future__ import annotations

import sqlite3
from typing import Any, Mapping

from .json import canonical_json


class SQLiteEventStore:
    """Append immutable events and retrieve them in durable sequence order."""

    def __init__(self, database: str = ":memory:") -> None:
        self._connection = sqlite3.connect(database)
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

    def all_events(self) -> list[tuple[int, str, str, str, str]]:
        rows = self._connection.execute(
            "SELECT sequence,event_id,event_type,timestamp,payload "
            "FROM events ORDER BY sequence"
        ).fetchall()
        return [(int(a), str(b), str(c), str(d), str(e)) for a, b, c, d, e in rows]

    def close(self) -> None:
        self._connection.close()
