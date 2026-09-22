from pathlib import Path
from uuid import uuid4

import pytest

from kernel.adapters.filesystem import FilesystemReadAdapter, FilesystemReadError
from kernel.authority import issue_authorization
from kernel.models import GovernanceDecision, Proposal


def make_authorization(root: Path, path: str, *, operation: str = "host.filesystem.read"):
    proposal = Proposal(
        id=uuid4(),
        request_id=uuid4(),
        principal_id=uuid4(),
        operation=operation,
        resource=str(root),
        parameters={"path": path},
    )
    return issue_authorization(
        proposal,
        GovernanceDecision("ALLOW", proposal.id, "test-policy", "permitted"),
        __import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        __import__("datetime").timedelta(minutes=1),
    ), proposal


def test_filesystem_read_is_constrained_to_root(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "allowed.txt").write_text("kernel", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")

    authorization, proposal = make_authorization(root, "allowed.txt")
    adapter = FilesystemReadAdapter(root)

    outcome = adapter.execute(authorization, proposal.parameters)

    assert outcome.status == "SUCCEEDED"
    assert outcome.evidence["path"] == "allowed.txt"
    assert outcome.evidence["size"] == 6
    assert outcome.evidence["sha256"]


def test_filesystem_read_rejects_path_escape(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (tmp_path / "outside.txt").write_text("secret", encoding="utf-8")

    authorization, proposal = make_authorization(root, "../outside.txt")

    with pytest.raises(FilesystemReadError, match="escapes"):
        FilesystemReadAdapter(root).execute(authorization, proposal.parameters)


def test_filesystem_read_rejects_absolute_path(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    target = root / "allowed.txt"
    target.write_text("kernel", encoding="utf-8")

    authorization, proposal = make_authorization(root, str(target))

    with pytest.raises(FilesystemReadError, match="absolute"):
        FilesystemReadAdapter(root).execute(authorization, proposal.parameters)


def test_filesystem_read_enforces_size_limit(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "large.txt").write_text("123456", encoding="utf-8")

    authorization, proposal = make_authorization(root, "large.txt")

    with pytest.raises(FilesystemReadError, match="exceeds"):
        FilesystemReadAdapter(root, max_bytes=5).execute(
            authorization, proposal.parameters
        )


def test_filesystem_read_rejects_wrong_operation(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "allowed.txt").write_text("kernel", encoding="utf-8")

    authorization, proposal = make_authorization(
        root, "allowed.txt", operation="host.filesystem.write"
    )

    with pytest.raises(FilesystemReadError, match="not for filesystem read"):
        FilesystemReadAdapter(root).execute(authorization, proposal.parameters)
