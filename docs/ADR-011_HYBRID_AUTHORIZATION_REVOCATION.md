# ADR-011: Hybrid Authorization Revocation

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Kernel uses both expiration and explicit durable revocation.

## Context
Expiration defines normal authorization lifetime. Expiration alone cannot address compromise or deliberate withdrawal before the deadline.

## Decision
An authorization becomes invalid when either its explicit expiration has passed or authoritative durable revocation applies.

Revocation MUST be attributable, durable, and auditable.

Revocation MUST NOT silently alter historical authorization evidence. It changes current validity.

Operations already in progress require explicit lifecycle semantics. Revocation cannot retroactively rewrite an already-recorded effect, but the execution boundary MUST prevent further consequential effects when current authority is invalid.

Expiration and revocation are distinct concepts and MUST remain distinguishable in evidence.
