# Kernel Concurrency and Transaction Boundary Model

Status: FOUNDATIONAL CONTRACT. Intended architecture, not implemented behavior.

## 1. Purpose

Concurrency can create authority races, duplicate effects, conflicting state, and misleading audit trails. Kernel therefore requires explicit transaction boundaries.

## 2. Authority Race

A valid authorization at time T1 does not automatically remain valid at T2.

The implementation must define which authorization properties are evaluated at authorization time and which are revalidated at execution time.

## 3. Concurrent Requests

Concurrent proposals for the same resource or operation MUST have defined conflict semantics.

The architecture MUST NOT depend on accidental thread/process ordering.

## 4. Duplicate Requests

Duplicate delivery MUST be distinguishable from independent operations where the operation requires idempotency.

## 5. Transaction Scope

The implementation must explicitly define whether each boundary is:

- atomic;
- transactional;
- eventually consistent;
- compensatable;
- inherently uncertain.

## 6. Event and State Coordination

If event persistence and state mutation are separate operations, the architecture MUST define recovery for every ordering:

event before state;
state before event;
event success/state failure;
state success/event failure;
partial commit.

## 7. Locking

Locks MAY protect consistency, but a lock is not authorization.

Holding a lock MUST NOT confer broader authority.

## 8. Time

Time-sensitive authorization requires a defined clock model and acceptable clock uncertainty.

System wall-clock time MUST NOT be assumed trustworthy for every security decision without an explicit assumption.

## 9. Distributed Operation

If Kernel spans processes or machines, message delivery, duplication, ordering, partition, and retry behavior become architectural concerns.

## 10. Accepted Architectural Decisions

- Transaction and event/state atomicity: ADR-012.
- Structured transport boundary: ADR-013.
- Idempotency: ADR-015.
- Global durable event ordering: ADR-016.
- Initial topology: ADR-023.

## 11. Remaining Implementation-Level Decisions

The implementation must still define the concrete transaction API, locking strategy, clock source and uncertainty bounds, identifier representation, SQLite sequence allocation, and any later distributed coordination mechanism.

These details MUST preserve the accepted authority, ordering, idempotency, durability, and recovery contracts. A future implementation choice that materially changes those contracts requires a new ADR.
