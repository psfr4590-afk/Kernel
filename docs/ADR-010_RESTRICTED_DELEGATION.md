# ADR-010: Restricted Delegation

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Delegation, when supported, is explicit, bounded, attributable, and no broader than the delegator's authority.

## Context
Unrestricted delegation chains create authority ambiguity and escalation risk.

## Decision
Delegation will be supported only as an explicit restricted authority transfer.

A delegation MUST identify the delegator, delegate, delegated operation and resource scope, validity interval, conditions or constraints, provenance, and delegation lineage.

A delegate MUST NOT receive authority broader than the delegator can legitimately confer.

Delegation MUST NOT silently extend authorization lifetime or scope. Delegated authority inherits the relevant expiration and cannot outlive the authority from which it derives.

Unlimited recursive delegation is not part of the base contract. If delegation chains are later required, each hop must preserve the same bounded semantics and remain independently auditable.
