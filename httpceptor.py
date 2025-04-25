import os
import ssl
from http.server import HTTPServer

from httpceptor import SimpleHTTPRequestHandler, sslcerts
from httpceptor.responses import mocked_responses

if __name__ == "__main__":
    server_address = ("0.0.0.0", int(os.getenv("SIMPLE_HTTP_PORT", "443")))
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)

    hosts = list(mocked_responses.keys())
    ca_key, ca_cert = sslcerts.generate_root_ca()
    server_cert, server_key = sslcerts.generate_server_cert(
        hosts, ca_key, ca_cert
    )

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print(
        f"Starting server on https://{server_address[0]}:{server_address[1]}"
    )
    server.serve_forever()
