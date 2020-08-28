import datetime
import uuid

import cryptography.hazmat.backends
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates
from cryptography.x509.oid import NameOID
from os import path

default_backend = cryptography.hazmat.backends.default_backend()


def cert_builder(
        public_key,
        common_name="CA Name",
        issuer=None,
        basic_constraints=x509.BasicConstraints(ca=True, path_length=None),
        key_usage=None,
        extended_key_usage=None,
        subject_alternative_names=None,
        not_valid_before=None,
        not_valid_after=None,
        valid_days=365,
):
    if not_valid_before is None:
        not_valid_before = datetime.datetime.utcnow()

    if not_valid_after is None:
        not_valid_after = not_valid_before + datetime.timedelta(days=valid_days)

    subject = cert_name(common_name)
    if issuer is None:
        issuer = subject

    builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).not_valid_before(
        not_valid_before
    ).not_valid_after(
        not_valid_after
    ).serial_number(
        int(uuid.uuid4())
    )

    if basic_constraints:
        builder = builder.add_extension(basic_constraints, critical=True)

    if key_usage is not None:
        builder = builder.add_extension(key_usage, critical=True)

    if extended_key_usage is not None:
        builder = builder.add_extension(extended_key_usage, critical=True)

    if subject_alternative_names is not None and len(subject_alternative_names) > 0:
        builder = builder.add_extension(
            x509.SubjectAlternativeName(subject_alternative_names),
            critical=True
        )

    return builder


def cert_key_usage(**kwargs):
    all_key_usages = [
        'digital_signature',
        'content_commitment',
        'key_encipherment',
        'data_encipherment',
        'key_agreement',
        'key_cert_sign',
        'crl_sign',
        'encipher_only',
        'decipher_only',
    ]
    for name in all_key_usages:
        kwargs.setdefault(name, False)

    return x509.KeyUsage(**kwargs)


def cert_extended_key_usage(**kwargs):
    extended_key_usages = {
        'server_auth': x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
        'client_auth': x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
        'code_signing': x509.oid.ExtendedKeyUsageOID.CODE_SIGNING,
        'email_protection': x509.oid.ExtendedKeyUsageOID.EMAIL_PROTECTION
        # ref:: https://cryptography.io/en/latest/_modules/cryptography/x509/oid/#ExtendedKeyUsageOID for details

    }
    res = []
    for k, v in kwargs.items():
        assert k in extended_key_usages, "specified exteneded key usage is not supported"
        if v:
            res.append(extended_key_usages[k])

    return x509.ExtendedKeyUsage(res)


def cert_name(common_name):
    return x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "KA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "bangalore"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])


def get_subject_alternate_names(**kwargs):
    subject_alt_names_list = {"othername": x509.OtherName,
                              "rfc822name": x509.RFC822Name,
                              "dnsname": x509.DNSName,
                              "directoryname": x509.DirectoryName,
                              "uniformresourceidentifier": x509.UniformResourceIdentifier,
                              "ipaddress": x509.IPAddress,
                              "registeredid": x509.RegisteredID}

    if len(kwargs) == 0:
        return None
    res = []
    for k, v in kwargs.items():
        assert k.lower() in subject_alt_names_list, "subject_alternate_names not supported." \
                                                    "Please provide from below list:\n" + ",".join(
            list(subject_alt_names_list.keys()))

        res.append(subject_alt_names_list[k](v))

    return res


def ca_cert_builder(public_key,
                    common_name="Root CA",
                    issuer=None,
                    basic_constraints=x509.BasicConstraints(
                        ca=True, path_length=None),
                    key_usage=cert_key_usage(
                        key_cert_sign=True),
                    extended_key_usage=None,
                    subject_alternative_names=None,
                    not_valid_before=None,
                    not_valid_after=None,
                    valid_days=3650,
                    ):
    return cert_builder(
        public_key=public_key,
        common_name=common_name,
        issuer=issuer,
        basic_constraints=basic_constraints,
        key_usage=key_usage,
        extended_key_usage=extended_key_usage,
        subject_alternative_names=subject_alternative_names,
        not_valid_before=not_valid_before,
        not_valid_after=not_valid_after,
        valid_days=valid_days,
    )


def user_cert_builder(
        public_key,
        common_name="User cert",
        issuer=None,
        basic_constraints=x509.BasicConstraints(
            ca=False, path_length=None),
        key_usage=cert_key_usage(
            key_cert_sign=False, digital_signature=True, key_encipherment=True),
        extended_key_usage=cert_extended_key_usage(server_auth=True),
        subject_alternative_names=get_subject_alternate_names(dnsname='localhost'),
        not_valid_before=None,
        not_valid_after=None,
        valid_days=3650,
):
    return cert_builder(
        public_key=public_key,
        common_name=common_name,
        issuer=issuer,
        basic_constraints=basic_constraints,
        key_usage=key_usage,
        extended_key_usage=extended_key_usage,
        subject_alternative_names=subject_alternative_names,
        not_valid_before=not_valid_before,
        not_valid_after=not_valid_after,
        valid_days=valid_days,
    )


def generate_rsa_private_key(key_size=2048, public_exponent=65537):
    cert_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend

    )
    return cert_key


def sign_cert(cert_builder, private_key, alg=None):
    alg = alg if alg else hashes.SHA256()
    return cert_builder.sign(
        private_key=private_key,
        algorithm=alg,
        backend=default_backend
    )


def convert_to_pem(cert):
    return cert.public_bytes(encoding=serialization.Encoding.PEM)


def create_root_ca_cert_pem(private_key):
    return convert_to_pem(
        sign_cert(ca_cert_builder(private_key.public_key(),
                                  key_usage=cert_key_usage(key_cert_sign=True, key_encipherment=True,
                                                           digital_signature=True),
                                  extended_key_usage=cert_extended_key_usage(email_protection=True)), private_key))


def convert_cert_to_p12(cert, root_cert_key, password="password"):
    return serialize_key_and_certificates(b'cert', root_cert_key, cert, None,
                                          serialization.BestAvailableEncryption(bytes(password, "utf-8")))


def save_key(key_data, file_name, password="password"):
    with open(file_name, "wb") as f:
        f.write(key_data.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(bytes(password, "utf-8"))
        ))


def load_key(filename, password="password"):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, bytes(password,"utf-8"), default_backend)
    return private_key


if __name__ == '__main__':
   #Sample usage
   #todo logging
    ca_key_file = "ca_cert_key.key"
    client_cert_key_file = "client_key.key"
    key_password = "123456"

    if path.isfile(ca_key_file):
        root_key = load_key(filename=ca_key_file, password=key_password)
    else:
        root_key = generate_rsa_private_key()
        save_key(root_key,ca_key_file, key_password)

    if path.isfile(client_cert_key_file):
        client_key = load_key(client_cert_key_file,key_password)
    else:
        client_key = generate_rsa_private_key()
        save_key(client_key,client_cert_key_file,key_password)

    ca = sign_cert(ca_cert_builder(root_key.public_key(),
                                   key_usage=cert_key_usage(key_cert_sign=True, key_encipherment=True,
                                                            digital_signature=True),
                                   extended_key_usage=cert_extended_key_usage(email_protection=True)), root_key)
    pem_file_data = convert_to_pem(ca)
    with open("ca_cert.pem", "wb") as f:
        f.write(pem_file_data)

    cert = sign_cert(user_cert_builder(client_key.public_key(),
                                       common_name="usercert", issuer=ca.issuer,
                                       subject_alternative_names=get_subject_alternate_names(
                                           rfc822name="testemail@example.com")), root_key)

    client_cert_p12Data = convert_cert_to_p12(cert, client_key, key_password)

    with open("usercert.p12", "wb") as f:
        f.write(client_cert_p12Data)
