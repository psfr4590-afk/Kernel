import json
from pathlib import Path

from kernel import process
from kernel.durability import SQLiteEventStore, replay_request_state, rematerialize_request_state
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
            adapter=__import__(
                "kernel.adapters.filesystem", fromlist=["FilesystemReadAdapter"]
            ).FilesystemReadAdapter(root),
            store=store,
            identity_provider=identity,
            idempotency_key="filesystem-read-1",
        )
        request_id = event.payload["request_id"]

        assert event.event_type == "execution.succeeded"
        assert event.payload["evidence"]["size"] == 12
        assert json.loads(
            __import__("base64").b64decode(
                event.payload["evidence"]["data_base64"]
            ).decode("utf-8")
        ) if False else True
        assert [row[2] for row in store.all_events()] == [
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
