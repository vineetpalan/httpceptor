# httpceptor

A lightweight HTTPS mock server built with Python.
It serves dynamic mock JSON responses based on the HTTP request's
hostname, method, and path. Ideal for API testing, mocking, and
simulating edge cases locally.

## Features

- 🔧 **Runtime-configurable REST endpoints** based on JSON config files.
- 🌐 **Supports multiple hostnames** via Subject Alternative Names (SAN).
- 🔐 **Secure HTTPS** with self-signed certificates.
- 🧪 **Mock responses** for `GET`, `POST`, `PUT`, `DELETE`, and `PATCH` requests.

---

## Installation

### Prerequisites

- Python 3.12+
- Install dependencies:

```bash
pip3.12 install -r requirements.txt
```

## Project Structure

```bash
.
├── httpceptor.py                  # Entrypoint: Starts HTTPS server
├── httpceptor/
│   ├── __init__.py                # Custom handler logic
│   ├── sslcerts.py                # SSL cert + Root CA generator
│   ├── responses.py               # Loads mock response JSONs
│   └── responses/                 # Folder for mock response JSON files
└── responses/                     # Folder for mock response JSON files
    └── *.json
```

- `httpceptor/`: Contains the server logic and mock responses.
- `responses/`: Contains the mock response JSON files.

## Usage

```shell
python3.12 httpceptor.py
```

By default, the server listens on port 443. You can specify a custom port using
the environment variable `SIMPLE_HTTP_PORT`:

```bash
export SIMPLE_HTTP_PORT=8443
python httpceptor.py
```

## Mock Response Configuration

Mock responses are defined in the `responses/` folder. Each file in this folder
must be a valid JSON file with the following structure:

```json
{
  "hello.example.com": {
    "/health": {
      "POST": {
        "return_code": 200,
        "response": "Healthy",
        "reason": "OK"
      }
    }
  }
}
```

You can define multiple files and routes per hostname.

## Generating SSL Certificates

### Root CA

To generate a root CA, use the `sslcerts.py` script. The server will use this
CA to sign server certificates.

### Server Certificates with SANs

The server certificates support multiple hostnames via Subject Alternative
Names (SAN). The generate_server_cert function will take a list of hostnames
and add them to the SAN field of the certificate.

## Example Usage with Docker Compose

We can use docker-compose setup to simulate a real-world client-server scenario
with hostname resolution and HTTPS.

### Setup Overview

- `httpceptor`: The mock HTTPS server container that:

  - Loads mock response definitions from the responses/ folder.

  - Uses TLS with a self-signed CA and server certificate.

  - Is accessible over a private IP 192.168.1.100.

- `client`: A simple container that:

  - Makes an HTTPS request to <https://hello.example.com/health>.

  - Resolves hello.example.com to the mock server's IP using /etc/hosts.

  - Trusts the server using the provided ca.crt.

### Networking Details

- `httpceptor` is assigned a static IP: 192.168.1.100.

- `client` uses Docker’s extra_hosts to resolve hello.example.com → 192.168.1.100.

- Both containers are on the same custom bridge network: httpceptor_network.

### Running the Example

```shell
docker-compose up --build
```

You should see curl from the client successfully connect to
<https://hello.example.com/health> using the custom CA certificate.

## License

MIT License
