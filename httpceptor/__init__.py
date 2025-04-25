"""
Simple HTTPS server that returns mocked JSON responses based
on hostname, method, and route.
"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from httpceptor.responses import mocked_responses


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Custom request handler that serves mock responses
    """

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def handle_request(self):
        parsed_path = urlparse(self.path)
        host = self.headers.get("Host", "").split(":")[0]
        route = parsed_path.path
        method = self.command
        try:
            response_data = mocked_responses[host][route][method].get(
                "response", ""
            )
            return_code = mocked_responses[host][route][method].get(
                "return_code", 200
            )
            reason = mocked_responses[host][route][method].get("reason")
            self.send_response(return_code, reason)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        except KeyError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
