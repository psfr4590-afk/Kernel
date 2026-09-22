import os
import sys

import pytest

from kernel.identity import IdentityError, LocalCryptographicIdentityProvider, verify_evidence


def test_local_cryptographic_identity_authenticates_attributable_principal():
    provider = LocalCryptographicIdentityProvider.generate()

    principal = provider.authenticate()
    evidence = provider.evidence()

    assert principal.authenticated is True
    assert principal.id == evidence.principal_id
    assert evidence.process_id == os.getpid()
    assert evidence.executable == sys.executable
    assert verify_evidence(evidence) == principal


def test_identity_evidence_rejects_tampered_signature():
    provider = LocalCryptographicIdentityProvider.generate()
    evidence = provider.evidence()
    tampered = type(evidence)(
        principal_id=evidence.principal_id,
        public_key=evidence.public_key,
        process_id=evidence.process_id,
        executable=evidence.executable,
        signature=evidence.signature[:-1] + bytes([evidence.signature[-1] ^ 1]),
    )

    with pytest.raises(IdentityError):
        verify_evidence(tampered)


def test_identity_evidence_rejects_different_process_binding():
    provider = LocalCryptographicIdentityProvider.generate()
    evidence = provider.evidence()
    tampered = type(evidence)(
        principal_id=evidence.principal_id,
        public_key=evidence.public_key,
        process_id=evidence.process_id + 1,
        executable=evidence.executable,
        signature=evidence.signature,
    )

    with pytest.raises(IdentityError):
        verify_evidence(tampered)
