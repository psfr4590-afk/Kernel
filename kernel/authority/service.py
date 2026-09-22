"""Authorization issuance and enforcement primitives."""

from __future__ import annotations

from datetime import datetime, timedelta

from kernel.models import Authorization, GovernanceDecision, Proposal, new_id
from kernel.authority.revocation import RevocationRegistry


class AuthorizationError(Exception):
    """Raised when authority cannot be established or validated."""


def issue_authorization(
    proposal: Proposal,
    decision: GovernanceDecision,
    now: datetime,
    lifetime: timedelta,
) -> Authorization:
    if decision.decision != "ALLOW":
        raise AuthorizationError("authorization requires an ALLOW governance decision")
    if decision.proposal_id != proposal.id:
        raise AuthorizationError("governance decision does not match proposal")
    if lifetime <= timedelta(0):
        raise AuthorizationError("authorization lifetime must be positive")
    return Authorization(
        id=new_id(),
        principal_id=proposal.principal_id,
        proposal_id=proposal.id,
        operation=proposal.operation,
        resource=proposal.resource,
        issued_at=now,
        expires_at=now + lifetime,
    )


def enforce_authorization(
    authorization: Authorization,
    proposal: Proposal,
    now: datetime,
    revocations: RevocationRegistry | None = None,
) -> None:
    if authorization.principal_id != proposal.principal_id:
        raise AuthorizationError("principal mismatch")
    if authorization.proposal_id != proposal.id:
        raise AuthorizationError("proposal mismatch")
    if authorization.operation != proposal.operation:
        raise AuthorizationError("operation outside authorization scope")
    if authorization.resource != proposal.resource:
        raise AuthorizationError("resource outside authorization scope")
    if not authorization.valid_at(now):
        raise AuthorizationError("authorization expired")
    if revocations is not None and revocations.is_revoked(authorization.id):
        raise AuthorizationError("authorization revoked")
