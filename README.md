# Kernel

## Model MechSuit: Foundational Sketch

Kernel is a proposed local-first governance and durability kernel for AI-driven systems.

Its central principle is:

> **Intelligence proposes; the kernel authorizes.**

Kernel is not the intelligence itself. It is the governed substrate between intelligence and consequential system effects. A model may reason, propose actions, request capabilities, and produce output. Those things do not become authority merely because a model produced them.

This repository begins as the **architectural sketch** of Kernel. It is intentionally documentation-first. The purpose of this stage is to establish the system's purpose, boundaries, vocabulary, invariants, evidence model, and architectural relationships before implementation decisions harden around incomplete assumptions.

## What Kernel is intended to provide

- Explicit identity and authority boundaries
- Governed execution rather than ambient authority
- Durable, auditable events and state
- Explicit authorization for consequential operations
- Separation between intelligence, policy, authority, execution, and persistence
- Observable system behavior suitable for reconstruction and review
- A foundation that can host different models or intelligence components without making any model the source of authority

## What Kernel is not

Kernel is not intended to be:

- an LLM runtime
- an agent framework
- a planner
- a crawler
- a RAG system
- a model provider
- a prompt system
- a tool catalog that grants authority by declaration

Those capabilities may exist elsewhere in a larger system. Kernel's responsibility is to govern the boundary where proposed intelligence becomes permitted system behavior.

## Foundational ordering

Kernel follows these architectural priorities:

1. Events before state
2. Identity before memory
3. Governance before autonomy
4. Observability before optimization

These are architectural principles, not implementation claims. The repository does not yet claim that a complete implementation exists.

## Current repository status

**Status: Architectural sketch / pre-implementation foundation**

The GitHub repository was intentionally started empty. The documents now being established here define the intended system before code is introduced.

See [Kernel Foundational Sketch](docs/KERNEL_SKETCH.md) for the initial architecture document.

