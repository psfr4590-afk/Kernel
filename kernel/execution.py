"""Effect-boundary orchestration."""

from __future__ import annotations

from collections.abc import Mapping

from kernel.authority import AuthorizationError, RevocationRegistry, enforce_authorization
from kernel.interfaces import ExecutionAdapter
from kernel.models import Authorization, Outcome, Proposal, new_id


class ExecutionProtocolError(RuntimeError):
    """Raised when an execution adapter returns an invalid terminal outcome."""


_TERMINAL_ADAPTER_STATUSES = frozenset({"SUCCEEDED", "FAILED", "PARTIAL"})


def execute(
    authorization: Authorization,
    proposal: Proposal,
    adapter: ExecutionAdapter,
    *,
    now,
    revocations: RevocationRegistry | None = None,
    on_attempt=None,
) -> Outcome:
    try:
        enforce_authorization(authorization, proposal, now, revocations)
    except AuthorizationError:
        return Outcome(new_id(), "BLOCKED", {"reason": "authorization rejected"})

    attempt_id = new_id()
    if on_attempt is not None:
        on_attempt(attempt_id)

    outcome = adapter.execute(authorization, proposal.parameters)
    if outcome.status not in _TERMINAL_ADAPTER_STATUSES:
        raise ExecutionProtocolError(
            f"execution adapter returned unsupported terminal status: {outcome.status!r}"
        )
    if not isinstance(outcome.evidence, Mapping):
        raise ExecutionProtocolError("execution adapter returned non-mapping evidence")

    return Outcome(attempt_id, outcome.status, dict(outcome.evidence))
