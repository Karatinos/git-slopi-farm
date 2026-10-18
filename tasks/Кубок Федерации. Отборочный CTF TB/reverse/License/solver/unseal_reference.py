#!/usr/bin/env python3
"""Reference decryptor for the client-side flag (organizer verification).

This documents the intended *offline / reverse* path. The primary intended solve
is dynamic (make the app show the flag after a valid PRO activation); this script
reproduces what the binary does internally so organizers can verify the flag and
so the intended reverse difficulty is documented.

The flag is protected client-side. This is bar-raising, not secrecy: a client
side flag is always recoverable by a competent reverser. What was removed is the
trivial path (labelled `FlagCt`/`KdfSalt` arrays + one-line AES-CBC). To recover
the flag statically a solver must read `Provisioning.Unseal` and replicate:

  token     = Tk XOR Mk                      (obfuscated admin token)
  h         = SHA256(token)                  (salt is derived, never stored)
  key       = SHA256(token || h)
  key       = SHA256(key   || h)   x ROUNDS  (custom key stretch)
  keystream = SHA256(key || Nn || counter_be32) ...   (concatenated)
  cipher    = Bl XOR keystream               (Bl is NOT a clean AES ciphertext)
  flag      = AES-CBC-decrypt(key, Iv, cipher)  then PKCS7-unpad

Usage:
    python unseal_reference.py [path/to/Secrets.g.cs]
Default path: ../../source/src/Generated/Secrets.g.cs
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ROUNDS = 6007
DEFAULT = Path(__file__).resolve().parents[2] / "source" / "src" / "Generated" / "Secrets.g.cs"


def _array(source: str, name: str) -> bytes:
    match = re.search(r"\b" + name + r"\s*=\s*\{([^}]*)\}", source, re.S)
    if not match:
        raise SystemExit(f"array '{name}' not found")
    return bytes(int(value, 16) for value in re.findall(r"0x[0-9A-Fa-f]{2}", match.group(1)))


def unseal(source: str) -> str:
    tk = _array(source, "Tk")
    mk = _array(source, "Mk")
    iv = _array(source, "Iv")
    nonce = _array(source, "Nn")
    blob = _array(source, "Bl")

    token = bytes(b ^ mk[i % len(mk)] for i, b in enumerate(tk))
    h = hashlib.sha256(token).digest()
    key = hashlib.sha256(token + h).digest()
    for _ in range(ROUNDS):
        key = hashlib.sha256(key + h).digest()

    keystream = bytearray()
    counter = 0
    while len(keystream) < len(blob):
        keystream += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1

    cipher = bytes(a ^ b for a, b in zip(blob, keystream))
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = decryptor.update(cipher) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded) + unpadder.finalize()).decode("utf-8")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    print(unseal(path.read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
