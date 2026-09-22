# Module and Package Topology

## Purpose

This is an implementation-neutral topology defining domain boundaries and dependency direction without selecting a language or framework.

## Logical domains

platform, resources, isolation, execution, scheduling, ipc, events, state, memory, persistence, identity, context, governance, authorization, security, configuration, recovery, observation, interfaces, intelligence_boundary, administration.

## Dependency direction

Platform -> Resources -> Isolation -> Execution.

Scheduling controls execution without becoming authority.

Requests enter through interfaces, then Identity/Context -> Proposal -> Governance -> Authorization -> Execution.

Execution produces Outcomes -> Events -> State.

Memory depends on explicit state/persistence and provenance contracts.

Recovery depends on durable evidence and governed execution.

Observation reads evidence and does not grant authority.

Administration changes configuration/governance through explicit authority.

Intelligence interacts through Proposal/Context interfaces and is not itself an authority source.

## Forbidden dependencies

A module MUST NOT bypass an authority boundary, infer permission from capability, mutate history through observation, bypass event recording for consequential effects, let model output directly invoke privileged execution, or let recovery silently gain broader authority.

## Critical boundaries

- Intelligence boundary: untrusted/generated intelligence versus Kernel authority.
- Governance boundary: proposal evaluation under policy.
- Authorization boundary: explicit bounded permission.
- Effect boundary: final enforcement point before consequential execution.
- Durability boundary: evidence sufficient for reconstruction claims.
- Observation boundary: inspection without mutation authority.

## Public and private interfaces

Public interfaces validate input and establish attribution. Internal interfaces may rely on documented upstream contracts only where those assumptions are enforceable.

Internal visibility is not authority.
