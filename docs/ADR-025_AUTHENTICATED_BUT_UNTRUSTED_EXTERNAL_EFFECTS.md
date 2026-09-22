# ADR-025: Authentication Without Inherent Trust

Status: ACCEPTED
Date: 2026-09-22
Decision owner: Project architecture

## Context

External systems may authenticate themselves or provide valid protocol responses without being inherently truthful, correct, safe, or authoritative.

## Decision

Kernel will treat external systems as **authenticated without granting inherent trust**.

Authentication establishes the identity or protocol-level origin that was successfully verified. It does not establish truthfulness, correctness, authorization, completion, or safety of the external effect.

External evidence must therefore carry explicit provenance and trust classification.

Where an external system reports an outcome, Kernel must distinguish authenticated reporting from independently established completion. Ambiguous external responses remain UNKNOWN where the evidence is insufficient.

## Architectural consequences

Kernel can integrate with authenticated services without turning authentication into an authority shortcut.

Trust decisions become operation-specific and evidence-based.

## Verification

Tests must cover valid authentication with false or conflicting outcome data, replay, stale responses, response loss, partial completion, impersonation, and unauthorized external effects.
