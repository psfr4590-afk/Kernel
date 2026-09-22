"""Effect-boundary orchestration."""

from __future__ import annotations

from kernel.authority import AuthorizationError, RevocationRegistry, enforce_authorization
from kernel.interfaces import ExecutionAdapter
from kernel.models import Authorization, Outcome, Proposal, new_id


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
    return adapter.execute(authorization, proposal.parameters)
