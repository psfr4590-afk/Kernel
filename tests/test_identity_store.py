from pathlib import Path

import pytest

from kernel.identity import IdentityError, LocalCryptographicIdentityProvider
from kernel.identity_store import IdentityKeyStore


def test_encrypted_identity_key_store_round_trip(tmp_path: Path) -> None:
    provider = LocalCryptographicIdentityProvider.generate()
    store = IdentityKeyStore(tmp_path / "identity.json")

    store.save(provider, passphrase="correct horse battery staple")
    restored = store.load(passphrase="correct horse battery staple")

    assert restored.authenticate().id == provider.authenticate().id
    assert restored.evidence().public_key == provider.evidence().public_key
    assert b"BEGIN" not in (tmp_path / "identity.json").read_bytes()


def test_encrypted_identity_key_store_rejects_wrong_passphrase(tmp_path: Path) -> None:
    store = IdentityKeyStore(tmp_path / "identity.json")
    store.save(
        LocalCryptographicIdentityProvider.generate(),
        passphrase="correct",
    )

    with pytest.raises(IdentityError):
        store.load(passphrase="wrong")


def test_encrypted_identity_key_store_detects_tampering(tmp_path: Path) -> None:
    path = tmp_path / "identity.json"
    store = IdentityKeyStore(path)
    store.save(LocalCryptographicIdentityProvider.generate(), passphrase="secret")

    data = bytearray(path.read_bytes())
    data[-2] = ord("A") if data[-2] != ord("A") else ord("B")
    path.write_bytes(bytes(data))

    with pytest.raises(IdentityError):
        store.load(passphrase="secret")


def test_identity_key_store_requires_passphrase(tmp_path: Path) -> None:
    store = IdentityKeyStore(tmp_path / "identity.json")
    provider = LocalCryptographicIdentityProvider.generate()

    with pytest.raises(IdentityError):
        store.save(provider, passphrase="")
