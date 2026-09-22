# ADR-013: Structured Pluggable Transport

- Status: ACCEPTED
- Date: 2026-09-22
- Decision: Kernel defines structured transport semantics independent of a single IPC mechanism; the initial implementation may use direct in-process calls.

## Context
Kernel may eventually span processes or machines, but choosing HTTP, sockets, or another transport now would prematurely couple authority semantics to deployment topology.

## Decision
Interfaces crossing a Kernel boundary MUST use structured, schema-validated messages with explicit identity, provenance, correlation, authorization context, and failure semantics.

The initial vertical slice SHOULD use direct Python calls where no trust boundary is crossed.

When a process or machine boundary is introduced, a transport adapter MUST preserve the same message and authority contracts.

No transport may create authority merely because it can deliver a message.
