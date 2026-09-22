"""Request intake and proposal construction."""

from __future__ import annotations

from typing import Any, Mapping

from kernel.models import Context, Principal, Proposal, Request, new_id, utc_now


class IntakeError(ValueError):
    """Raised when an incoming request cannot become a valid proposal."""


def receive_request(
    principal: Principal,
    *,
    operation: str,
    resource: str,
    parameters: Mapping[str, Any],
) -> Request:
    if not principal.authenticated:
        raise IntakeError("unauthenticated principal cannot submit a request")
    if not operation or not resource:
        raise IntakeError("operation and resource are required")
    return Request(
        id=new_id(),
        principal_id=principal.id,
        operation=operation,
        resource=resource,
        parameters=dict(parameters),
        received_at=utc_now(),
        idempotency_key=str(new_id()),
    )


def build_proposal(request: Request) -> Proposal:
    return Proposal(
        id=new_id(),
        request_id=request.id,
        principal_id=request.principal_id,
        operation=request.operation,
        resource=request.resource,
        parameters=dict(request.parameters),
    )


def capture_context(principal: Principal, resource: str) -> Context:
    return Context(
        id=new_id(),
        principal_id=principal.id,
        resource=resource,
        captured_at=utc_now(),
    )
