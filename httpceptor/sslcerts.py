import os
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

CERTS_DIR = os.getenv("CERTS_DIR")

def save_pem(obj, filename, encoding, private=False, password=None):
    if private:
        pem = obj.private_bytes(
            encoding=encoding,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=(
                serialization.NoEncryption()
                if not password
                else serialization.BestAvailableEncryption(password.encode())
            ),
        )
    else:
        pem = obj.public_bytes(encoding)
    with open(f"{CERTS_DIR}/{filename}", "wb") as f:
        f.write(pem)
    print(f"Saved: {CERTS_DIR}/{filename}")


def generate_root_ca(ca_name="My Root CA", valid_days=3650):
    # Generate private key
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create self-signed CA cert
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, ca_name),
            x509.NameAttribute(NameOID.COMMON_NAME, ca_name),
        ]
    )
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(tz=timezone.utc))
        .not_valid_after(
            datetime.now(tz=timezone.utc) + timedelta(days=valid_days)
        )
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )
    save_pem(ca_key, "ca.key", serialization.Encoding.PEM, private=True)
    save_pem(ca_cert, "ca.crt", serialization.Encoding.PEM)
    return ca_key, ca_cert


def generate_server_cert(
    hostnames, ca_key, ca_cert, valid_days=365, filename="server"
):

    # Generate private key
    server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Set subject using the first hostname
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Local Server"),
            x509.NameAttribute(NameOID.COMMON_NAME, hostnames[0]),
        ]
    )

    # SAN: add all provided hostnames
    san = x509.SubjectAlternativeName(
        [x509.DNSName(name) for name in hostnames]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(tz=timezone.utc))
        .not_valid_after(
            datetime.now(tz=timezone.utc) + timedelta(days=valid_days)
        )
        .add_extension(san, critical=False)
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

    # Save to PEM
    certfile = f"{CERTS_DIR}/{filename}.crt"
    keyfile = f"{CERTS_DIR}/{filename}.key"

    with open(certfile, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    with open(keyfile, "wb") as f:
        f.write(
            server_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )

    return certfile, keyfile
