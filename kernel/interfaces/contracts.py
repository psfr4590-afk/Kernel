"""Explicit contracts at the first vertical slice boundaries."""

from __future__ import annotations

from datetime import datetime
from typing import Mapping, Protocol, Any

from kernel.models import (
    Authorization,
    Context,
    GovernanceDecision,
    Outcome,
    Principal,
    Proposal,
)


class GovernanceEvaluator(Protocol):
    def evaluate(
        self,
        proposal: Proposal,
        context: Context,
    ) -> GovernanceDecision:
        """Return a governed decision. Policy mechanism remains implementation-defined."""


class ExecutionAdapter(Protocol):
    def execute(
        self,
        authorization: Authorization,
        parameters: Mapping[str, Any],
    ) -> Outcome:
        """Execute only within the exact authorization boundary."""


class Clock(Protocol):
    def now(self) -> datetime:
        """Return the authoritative Kernel time source."""


class IdentityProvider(Protocol):
    def authenticate(self) -> Principal:
        """Return an attributable principal or fail closed."""
