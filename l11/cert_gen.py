"""Generate two keypairs for use in Lab 11.

This code is based on the example found at
https://nachtimwald.com/2019/12/10/python-http-server/.
"""

import gen_certificate


def make_key(cert_name, key_name):
    """Generate a public/private keypair for the user.

    These files will be placed in the same directory as this file.
    """
    # Generate the public certificate and private key
    tls_cert, tls_key = gen_certificate.gen_self_signed_cert()

    # Save the certificate (which contains the public key)
    cert_file = open(cert_name, "w")
    cert_file.write(tls_cert.decode('ascii'))
    cert_file.close()

    # Save the private key
    key_file = open(key_name, "w")
    key_file.write(tls_key.decode('ascii'))
    key_file.close()


if __name__ == "__main__":
    # Create keypairs for the client and server
    make_key("cli_cert.crt", "cli_key.key")  # Client
    make_key("srv_cert.crt", "srv_key.key")  # Server