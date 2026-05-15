import os
import socket
import threading
from pathlib import Path

from aes_socket_utils import (
    encrypt_aes_cbc,
    build_key_packet,
    build_data_packet,
    parse_key_packet,
    parse_length_header,
    LENGTH_HEADER_SIZE,
    recv_exact,
    decrypt_aes_cbc,
)


def _receiver_thread(host, key_port, data_port, results, timeout=10):
    """Thread function to receive key and data, decrypt and store plaintext."""
    try:
        # KEY_PORT
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout)
            server.bind((host, key_port))
            server.listen(1)
            conn, _ = server.accept()
            with conn:
                conn.settimeout(timeout)
                header = recv_exact(conn, 4)
                key_len = int.from_bytes(header, "big")
                rest = recv_exact(conn, key_len + 16)
                key_packet = header + rest

        key, iv = parse_key_packet(key_packet)

        # DATA_PORT
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout)
            server.bind((host, data_port))
            server.listen(1)
            conn, _ = server.accept()
            with conn:
                conn.settimeout(timeout)
                len_header = recv_exact(conn, LENGTH_HEADER_SIZE)
                length = parse_length_header(len_header)
                ciphertext = recv_exact(conn, length)

        plaintext = decrypt_aes_cbc(key, iv, ciphertext)
        results["plaintext"] = plaintext
        results["success"] = True
    except Exception as e:
        results["error"] = str(e)
        results["success"] = False


def _sender_send(host, key_port, data_port, message, timeout=10):
    """Send a message using the same protocol as sender.py."""
    plaintext = message.encode("utf-8")
    key, iv, ciphertext = encrypt_aes_cbc(plaintext, key_size=16)

    key_packet = build_key_packet(key, iv)
    data_packet = build_data_packet(ciphertext)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, key_port))
        sock.sendall(key_packet)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, data_port))
        sock.sendall(data_packet)


def test_local_sender_receiver_roundtrip():
    """Full local roundtrip: send -> receive -> decrypt -> verify."""
    host = "127.0.0.1"
    key_port = 18710
    data_port = 18711
    message = "Xin chao FIT4012 - Lab 6 AES Socket local test"

    results = {}
    receiver = threading.Thread(
        target=_receiver_thread, args=(host, key_port, data_port, results), daemon=True
    )

    receiver.start()
    _sender_send(host, key_port, data_port, message)
    receiver.join(timeout=10)

    assert results.get("success"), f"Receiver failed: {results.get('error')}"
    assert results["plaintext"] == message.encode("utf-8"), (
        f"Plaintext mismatch: {results['plaintext']} != {message}"
    )
