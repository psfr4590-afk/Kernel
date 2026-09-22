"""Kernel governed execution and durability core."""

from .identity import IdentityError, IdentityEvidence, LocalCryptographicIdentityProvider, verify_evidence
from .pipeline import process

__version__ = "0.1.0"

__all__ = ["process", "__version__"]
