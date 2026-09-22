"""Cryptographic identity and local process binding."""

from __future__ import annotations

import hashlib
import os
import sys
from dataclasses import dataclass
from uuid import UUID

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from kernel.models import Principal


class IdentityError(ValueError):
    """Raised when cryptographic identity cannot be authenticated."""


@dataclass(frozen=True)
class IdentityEvidence:
    principal_id: UUID
    public_key: bytes
    process_id: int
    executable: str
    signature: bytes


class LocalCryptographicIdentityProvider:
    """Authenticate one local principal using Ed25519 plus process binding."""

    def __init__(
        self,
        private_key: Ed25519PrivateKey,
        *,
        kind: str = "local-process",
    ) -> None:
        self._private_key = private_key
        self._kind = kind

    @classmethod
    def generate(cls, *, kind: str = "local-process") -> "LocalCryptographicIdentityProvider":
        return cls(Ed25519PrivateKey.generate(), kind=kind)

    def authenticate(self) -> Principal:
        public_key = self._private_key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        principal_id = UUID(bytes=hashlib.sha256(public_bytes).digest()[:16])
        binding = self._binding()
        signature = self._private_key.sign(binding)
        try:
            public_key.verify(signature, binding)
        except Exception as exc:
            raise IdentityError("cryptographic identity verification failed") from exc
        if not self._verify_process_binding(binding):
            raise IdentityError("local process binding verification failed")
        return Principal(principal_id, self._kind, authenticated=True)

    def evidence(self) -> IdentityEvidence:
        public_key = self._private_key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        binding = self._binding()
        signature = self._private_key.sign(binding)
        return IdentityEvidence(
            principal_id=UUID(bytes=hashlib.sha256(public_bytes).digest()[:16]),
            public_key=public_bytes,
            process_id=os.getpid(),
            executable=sys.executable,
            signature=signature,
        )

    def _binding(self) -> bytes:
        executable = os.path.abspath(sys.executable).encode("utf-8")
        return b"kernel-process-binding-v1\0" + str(os.getpid()).encode("ascii") + b"\0" + executable

    def _verify_process_binding(self, binding: bytes) -> bool:
        expected = (
            b"kernel-process-binding-v1\0"
            + str(os.getpid()).encode("ascii")
            + b"\0"
            + os.path.abspath(sys.executable).encode("utf-8")
        )
        return binding == expected


def verify_evidence(evidence: IdentityEvidence) -> Principal:
    """Verify cryptographic identity evidence and its local process binding."""
    public_key = Ed25519PublicKey.from_public_bytes(evidence.public_key)
    binding = (
        b"kernel-process-binding-v1\0"
        + str(evidence.process_id).encode("ascii")
        + b"\0"
        + os.path.abspath(evidence.executable).encode("utf-8")
    )
    try:
        public_key.verify(evidence.signature, binding)
    except Exception as exc:
        raise IdentityError("identity evidence signature is invalid") from exc
    if evidence.process_id != os.getpid() or os.path.abspath(evidence.executable) != os.path.abspath(sys.executable):
        raise IdentityError("identity evidence is bound to another local process")
    expected_id = UUID(bytes=hashlib.sha256(evidence.public_key).digest()[:16])
    if evidence.principal_id != expected_id:
        raise IdentityError("identity principal does not match public key")
    return Principal(evidence.principal_id, "local-process", authenticated=True)
