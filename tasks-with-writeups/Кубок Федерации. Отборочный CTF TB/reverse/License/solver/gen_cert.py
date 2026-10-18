#!/usr/bin/env python3
"""Create a self-signed certificate for the local CTF activation solver."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def main() -> int:
    parser = argparse.ArgumentParser(description="Create cert.pem and key.pem for an activation hostname.")
    parser.add_argument("host", help="Activation hostname, for example activation.example.ru")
    parser.add_argument("--cert", type=Path, default=Path(__file__).with_name("cert.pem"))
    parser.add_argument("--key", type=Path, default=Path(__file__).with_name("key.pem"))
    args = parser.parse_args()

    host = args.host.strip().lower().rstrip(".")
    if not host or "/" in host or ":" in host:
        parser.error("host must be a hostname without a scheme, path, or port")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host)])
    now = datetime.now(timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(host)]), critical=False)
        .sign(private_key, hashes.SHA256())
    )

    args.key.write_bytes(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )
    args.cert.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    print(f"Created {args.cert} and {args.key} for {host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
