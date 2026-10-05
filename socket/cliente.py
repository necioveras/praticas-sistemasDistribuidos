#!/usr/bin/env python3
"""Interactive Python 3.11 WebSocket client for the Java chat server."""

import argparse
import asyncio
import os
import ssl
import sys
from pathlib import Path
from urllib.parse import urlsplit

from websockets.asyncio.client import connect
from websockets.exceptions import WebSocketException


DEFAULT_URL = "wss://753a84e2-6e13-4f64-aa73-1e5ccacb118a-00-vk0dsmua3qdl.riker.replit.dev/ws"


def create_ssl_context() -> ssl.SSLContext:
    """Use normal TLS verification and include the workspace's system CA bundle."""
    context = ssl.create_default_context()
    configured_bundle = os.environ.get("SSL_CERT_FILE")
    candidates = [
        configured_bundle,
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
    ]

    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            context.load_verify_locations(cafile=candidate)
            break

    return context


async def chat(endpoint: str) -> None:
    parsed = urlsplit(endpoint)
    if parsed.scheme not in {"ws", "wss"} or not parsed.hostname:
        raise ValueError("Informe uma URL WebSocket completa, começando com ws:// ou wss://.")
    if parsed.path != "/ws":
        raise ValueError("O endpoint do servidor Java termina em /ws.")

    connection_options = {"open_timeout": 10}
    if parsed.scheme == "wss":
        connection_options["ssl"] = create_ssl_context()

    async with connect(endpoint, **connection_options) as websocket:
        greeting = await asyncio.wait_for(websocket.recv(), timeout=10)
        print(greeting)

        while True:
            try:
                message = await asyncio.to_thread(input, "> ")
            except EOFError:
                print()
                return

            await websocket.send(message)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
            except TimeoutError:
                print("O servidor não respondeu dentro de 10 segundos.", file=sys.stderr)
                return

            print(response)
            if message.strip().lower() == "exit":
                return


def main() -> int:
    parser = argparse.ArgumentParser(description="Conecte-se ao servidor Java WebSocket.")
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_URL,
        help=f"URL do servidor (padrão: {DEFAULT_URL})",
    )
    args = parser.parse_args()

    try:
        asyncio.run(chat(args.url))
    except KeyboardInterrupt:
        print("\nCliente encerrado.")
    except (OSError, TimeoutError, ValueError, WebSocketException, ssl.SSLError) as error:
        print(f"Falha na conexão WebSocket: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
