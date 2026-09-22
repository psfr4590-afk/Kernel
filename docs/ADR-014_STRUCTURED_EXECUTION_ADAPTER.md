# ADR-014: Structured Execution Adapter

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Consequential execution occurs through a structured operation adapter contract.

## Context
The execution boundary is where authorization must become enforceable effect control. Arbitrary commands or unrestricted callables would undermine that property.

## Decision
An execution adapter receives a validated, authorized operation with attributable principal, bounded operation/resource scope, validated parameters, authorization identity and validity, required resource limits, and correlation/provenance data.

The adapter MUST NOT infer broader authority from caller identity, model output, role text, or transport metadata.

The adapter MUST return a defined execution outcome, including uncertainty where completion cannot be established.

The interface MUST preserve enough evidence to distinguish blocked, not attempted, attempted, succeeded, failed, partial, and unknown outcomes.
