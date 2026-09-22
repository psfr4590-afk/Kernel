"""Effect-boundary orchestration."""

from __future__ import annotations

from typing import Any, Mapping

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
) -> Outcome:
    try:
        enforce_authorization(authorization, proposal, now, revocations)
    except AuthorizationError:
        return Outcome(new_id(), "BLOCKED", {"reason": "authorization rejected"})
    return adapter.execute(authorization, proposal.parameters)
