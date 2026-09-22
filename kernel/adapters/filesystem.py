"""Constrained host filesystem read adapter for the first vertical slice."""

from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
from typing import Any, Mapping

from kernel.models import Authorization, Outcome, new_id


class FilesystemReadError(ValueError):
    """Raised when a filesystem read violates the adapter boundary."""


class FilesystemReadAdapter:
    """Read existing regular files beneath one explicitly configured root."""

    def __init__(
        self,
        root: str | os.PathLike[str],
        *,
        max_bytes: int = 1024 * 1024,
    ) -> None:
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        self._root = Path(root).resolve(strict=True)
        if not self._root.is_dir():
            raise FilesystemReadError("filesystem root must be a directory")
        self._max_bytes = max_bytes

    @property
    def root(self) -> Path:
        return self._root

    def execute(
        self,
        authorization: Authorization,
        parameters: Mapping[str, Any],
    ) -> Outcome:
        if authorization.operation != "host.filesystem.read":
            raise FilesystemReadError("authorization is not for filesystem read")
        if Path(authorization.resource).resolve() != self._root:
            raise FilesystemReadError("authorization resource is outside adapter root")

        relative_path = parameters.get("path")
        if not isinstance(relative_path, str) or not relative_path:
            raise FilesystemReadError("filesystem read requires a relative path")
        if "\x00" in relative_path:
            raise FilesystemReadError("filesystem path contains a NUL byte")

        candidate = self._resolve_safe_path(relative_path)
        try:
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(candidate, flags)
            with os.fdopen(descriptor, "rb") as handle:
                data = handle.read(self._max_bytes + 1)
        except OSError as exc:
            raise FilesystemReadError("filesystem read failed") from exc

        if len(data) > self._max_bytes:
            raise FilesystemReadError("filesystem read exceeds configured limit")

        return Outcome(
            new_id(),
            "SUCCEEDED",
            {
                "path": relative_path,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "data_base64": base64.b64encode(data).decode("ascii"),
            },
        )

    def _resolve_safe_path(self, relative_path: str) -> Path:
        requested = Path(relative_path)
        if requested.is_absolute():
            raise FilesystemReadError("absolute filesystem paths are not permitted")
        try:
            candidate = requested.resolve()
            if not candidate.is_relative_to(self._root):
                raise FilesystemReadError("filesystem path escapes configured root")
            if not candidate.is_file():
                raise FilesystemReadError("filesystem target must be a regular file")
            return candidate
        except OSError as exc:
            raise FilesystemReadError("filesystem path cannot be resolved") from exc
