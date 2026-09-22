"""Encrypted local storage for Kernel cryptographic identity keys."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Final

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from kernel.identity import IdentityError, LocalCryptographicIdentityProvider

_FORMAT_VERSION: Final = 1
_SALT_SIZE: Final = 16
_NONCE_SIZE: Final = 12
_KEY_SIZE: Final = 32
_SCRYPT_N: Final = 2**14
_SCRYPT_R: Final = 8
_SCRYPT_P: Final = 1


class IdentityKeyStore:
    """Persist one local identity private key encrypted with AES-256-GCM."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = Path(path)

    def save(
        self,
        provider: LocalCryptographicIdentityProvider,
        *,
        passphrase: str,
    ) -> None:
        if not passphrase:
            raise IdentityError("identity key store passphrase is required")
        private_key = provider.export_private_key()
        salt = os.urandom(_SALT_SIZE)
        nonce = os.urandom(_NONCE_SIZE)
        key = self._derive_key(passphrase, salt)
        plaintext = private_key
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, self._aad())
        envelope = {
            "format_version": _FORMAT_VERSION,
            "kdf": {
                "name": "scrypt",
                "n": _SCRYPT_N,
                "r": _SCRYPT_R,
                "p": _SCRYPT_P,
            },
            "cipher": {"name": "AES-256-GCM"},
            "salt": self._b64(salt),
            "nonce": self._b64(nonce),
            "ciphertext": self._b64(ciphertext),
        }
        encoded = json.dumps(
            envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fd = os.open(self._path, flags, 0o600)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(encoded)
        except Exception:
            try:
                os.close(fd)
            except OSError:
                pass
            raise
        try:
            os.chmod(self._path, 0o600)
        except OSError:
            pass

    def load(
        self,
        *,
        passphrase: str,
    ) -> LocalCryptographicIdentityProvider:
        if not passphrase:
            raise IdentityError("identity key store passphrase is required")
        try:
            envelope = json.loads(self._path.read_text(encoding="ascii"))
            if envelope.get("format_version") != _FORMAT_VERSION:
                raise IdentityError("unsupported identity key store format")
            kdf = envelope.get("kdf", {})
            if (
                kdf.get("name") != "scrypt"
                or kdf.get("n") != _SCRYPT_N
                or kdf.get("r") != _SCRYPT_R
                or kdf.get("p") != _SCRYPT_P
            ):
                raise IdentityError("unsupported identity key store parameters")
            if envelope.get("cipher", {}).get("name") != "AES-256-GCM":
                raise IdentityError("unsupported identity key store cipher")
            salt = self._unb64(envelope["salt"])
            nonce = self._unb64(envelope["nonce"])
            ciphertext = self._unb64(envelope["ciphertext"])
            if len(salt) != _SALT_SIZE or len(nonce) != _NONCE_SIZE:
                raise IdentityError("invalid identity key store envelope")
            key = self._derive_key(passphrase, salt)
            private_key = AESGCM(key).decrypt(nonce, ciphertext, self._aad())
            return LocalCryptographicIdentityProvider.from_private_key(private_key)
        except IdentityError:
            raise
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise IdentityError("identity key store could not be loaded") from exc
        except Exception as exc:
            raise IdentityError("identity key store authentication failed") from exc

    @staticmethod
    def _derive_key(passphrase: str, salt: bytes) -> bytes:
        return Scrypt(
            salt=salt,
            length=_KEY_SIZE,
            n=_SCRYPT_N,
            r=_SCRYPT_R,
            p=_SCRYPT_P,
        ).derive(passphrase.encode("utf-8"))

    @staticmethod
    def _aad() -> bytes:
        return b"kernel-identity-key-store-v1"

    @staticmethod
    def _b64(value: bytes) -> str:
        return base64.b64encode(value).decode("ascii")

    @staticmethod
    def _unb64(value: str) -> bytes:
        return base64.b64decode(value.encode("ascii"), validate=True)
