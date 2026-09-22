import base64
from pathlib import Path

from kernel import process
from kernel.adapters.filesystem import FilesystemReadAdapter
from kernel.durability import (
    SQLiteEventStore,
    assess_request_recovery,
    replay_request_state,
    rematerialize_request_state,
)
from kernel.identity import LocalCryptographicIdentityProvider
from kernel.models import GovernanceDecision


class AllowFilesystemRead:
    def evaluate(self, proposal, context):
        return GovernanceDecision(
            "ALLOW", proposal.id, "filesystem-v1", "read permitted"
        )


def test_complete_host_filesystem_read_vertical_slice(tmp_path: Path) -> None:
    database = tmp_path / "kernel.db"
    root = tmp_path / "allowed"
    root.mkdir()
    target = root / "hello.txt"
    target.write_text("hello kernel", encoding="utf-8")

    identity = LocalCryptographicIdentityProvider.generate()
    store = SQLiteEventStore(str(database))
    try:
        event = process(
            operation="host.filesystem.read",
            resource=str(root),
            parameters={"path": "hello.txt"},
            governance=AllowFilesystemRead(),
            adapter=FilesystemReadAdapter(root),
            store=store,
            identity_provider=identity,
            idempotency_key="filesystem-read-1",
        )
        request_id = event.payload["request_id"]

        assert event.event_type == "execution.succeeded"
        assert event.payload["evidence"]["size"] == 12
        assert base64.b64decode(
            event.payload["evidence"]["data_base64"]
        ) == b"hello kernel"
        events = store.all_events()
        assert [row[2] for row in events] == [
            "operation.claimed",
            "authorization.issued",
            "execution.attempted",
            "execution.succeeded",
        ]
        assert all(store.verify_event_integrity(row[0]) for row in store.all_events())
        state = replay_request_state(store.all_events(), request_id)
        assert state["status"] == "SUCCEEDED"
        assert state["evidence"]["sha256"] == event.payload["evidence"]["sha256"]
    finally:
        store.close()

    reopened = SQLiteEventStore(str(database))
    try:
        duplicate = process(
            operation="host.filesystem.read",
            resource=str(root),
            parameters={"path": "hello.txt"},
            governance=AllowFilesystemRead(),
            adapter=__import__(
                "kernel.adapters.filesystem", fromlist=["FilesystemReadAdapter"]
            ).FilesystemReadAdapter(root),
            store=reopened,
            identity_provider=identity,
            idempotency_key="filesystem-read-1",
        )
        assert duplicate.sequence == event.sequence
        assert len(reopened.all_events()) == 4

        assessment = rematerialize_request_state(reopened, request_id)
        assert assessment.status == "SUCCEEDED"
        assert reopened.get_state(request_id)[1] == event.sequence
    finally:
        reopened.close()


class TerminalWriteFailStore(SQLiteEventStore):
    def append_with_state(self, **kwargs):
        if kwargs["event_type"].startswith("execution."):
            raise OSError("simulated terminal persistence failure")
        return super().append_with_state(**kwargs)


def test_filesystem_read_effect_without_terminal_persistence_is_unknown(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    (root / "hello.txt").write_text("hello kernel", encoding="utf-8")

    identity = LocalCryptographicIdentityProvider.generate()
    store = TerminalWriteFailStore()
    try:
        try:
            process(
                operation="host.filesystem.read",
                resource=str(root),
                parameters={"path": "hello.txt"},
                governance=AllowFilesystemRead(),
                adapter=FilesystemReadAdapter(root),
                store=store,
                identity_provider=identity,
                idempotency_key="filesystem-read-persistence-failure",
            )
        except OSError as exc:
            assert "terminal persistence failure" in str(exc)
        else:
            raise AssertionError("terminal persistence failure was not raised")

        claimed = store.all_events()[0]
        request_id = __import__("json").loads(claimed[4])["request_id"]
        assert [row[2] for row in store.all_events()] == [
            "operation.claimed",
            "authorization.issued",
            "execution.attempted",
        ]
        assessment = assess_request_recovery(store.all_events(), request_id)
        assert assessment.status == "UNKNOWN"
        assert assessment.requires_reconciliation is True
    finally:
        store.close()
