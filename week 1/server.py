"""
log_server_simulator.py
------------------------
Simulates three Netflix regional streaming servers that continuously
generate application logs over TCP connections.

Run this file first and keep it running.
"""

import socket
import threading
import random
import time
from datetime import datetime

# Netflix regional servers
SERVERS = [
    ("netflix-india", 9001),
    ("netflix-usa", 9002),
    ("netflix-europe", 9003),
]

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Netflix log message templates
MESSAGE_TEMPLATES = {
    "INFO": [
        "User#{uid} logged in successfully",
        "Movie#{mid} playback started",
        "Movie#{mid} playback completed",
        "Subscription renewed successfully",
        "User#{uid} added Movie#{mid} to Watchlist",
    ],

    "WARNING": [
        "Slow internet detected for User#{uid}",
        "Buffering detected during Movie#{mid}",
        "High streaming traffic in region",
        "Subtitle loading delayed for Movie#{mid}",
    ],

    "ERROR": [
        "Playback failed for Movie#{mid}",
        "Payment failed for User#{uid}",
        "Authentication failed for User#{uid}",
        "Content server unavailable",
        "Video stream interrupted for Movie#{mid}",
    ],

    "DEBUG": [
        "Cache refreshed for Movie#{mid}",
        "Recommendation engine executed",
        "Fetching metadata for Movie#{mid}",
        "CDN node switched successfully",
    ],
}


def build_log_line(server_name):
    """Generate one Netflix log entry."""

    level = random.choice(LEVELS)
    uid = random.randint(1000, 9999)
    mid = random.randint(100, 999)

    message = random.choice(MESSAGE_TEMPLATES[level]).format(
        uid=uid,
        mid=mid
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"{timestamp} | {level} | {server_name} | {message}\n"


def handle_client(conn, server_name):
    """Continuously send log entries."""

    print(f"[{server_name}] Harvester connected...")

    try:
        while True:
            log = build_log_line(server_name)
            conn.sendall(log.encode("utf-8"))

            # Random delay
            time.sleep(random.uniform(0.05, 0.4))

            # Send corrupted data occasionally
            if random.random() < 0.05:
                conn.sendall(b"INVALID_NETFLIX_LOG_RECORD\n")

    except (BrokenPipeError, ConnectionResetError):
        print(f"[{server_name}] Harvester disconnected.")

    finally:
        conn.close()


def run_server(server_name, port):
    """Start one Netflix regional server."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("127.0.0.1", port))
    sock.listen(1)

    print(f"[{server_name}] Listening on port {port}...")

    while True:
        conn, addr = sock.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, server_name),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":

    threads = []

    for name, port in SERVERS:
        t = threading.Thread(
            target=run_server,
            args=(name, port),
            daemon=True
        )

        t.start()
        threads.append(t)

    print("\nNetflix Log Server Simulator is running...")
    print("Streaming logs from all regional servers.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping Netflix Log Server Simulator...")