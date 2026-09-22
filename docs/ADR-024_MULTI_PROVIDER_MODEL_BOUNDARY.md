# ADR-024: Multiple Model Providers Behind the Intelligence Boundary

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

Kernel is intended to govern interchangeable intelligence components rather than become dependent on a single model provider.

## Decision

Kernel will support **multiple model providers behind explicit intelligence boundaries**.

Each provider integration must be treated as an untrusted intelligence component until its output crosses the Kernel proposal/validation boundary.

Provider-specific identity, capabilities, resource limits, input/output handling, provenance, failure behavior, and isolation must be explicit.

No provider receives Kernel authority merely because it is registered, selected, trusted by configuration, or previously used successfully.

Provider replacement must not change durable Kernel authority semantics.

## Verification

Tests must cover provider substitution, malformed output, provider impersonation, provider failure, resource exhaustion, provenance, unauthorized effect attempts, and cross-provider authority leakage.
