"""Authority and identity boundaries."""

from .revocation import RevocationRegistry, SQLiteRevocationRegistry
from .service import AuthorizationError, enforce_authorization, issue_authorization

__all__ = [
    "AuthorizationError",
    "RevocationRegistry",
    "enforce_authorization",
    "issue_authorization",
]
