"""
log_harvester_daemon.py
-----------------------
Netflix Distributed Log Harvester

This program connects to multiple Netflix regional servers,
collects streaming logs in real time, validates them,
and stores them as compact binary records in partition files.

Workflow:
1. Connects to each Netflix regional server.
2. Reads raw TCP log streams.
3. Validates each log using Regular Expressions.
4. Converts valid logs into structured records.
5. Dynamically creates binary partition files based on
   (server, log level).
6. Stores logs in compact binary format.
"""

import socket
import threading
import re
import struct
import os
import time
from collections import defaultdict

# Netflix Servers
SERVERS = [
    ("netflix-india", 9001),
    ("netflix-usa", 9002),
    ("netflix-europe", 9003),
]

HOST = "127.0.0.1"
PARTITION_DIR = "partitions"

# Log Validation Pattern
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG)\s*\|\s*"
    r"(?P<service>[\w\-]+)\s*\|\s*"
    r"(?P<message>.+)$"
)

LEVEL_CODE = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
}

CODE_LEVEL = {v: k for k, v in LEVEL_CODE.items()}

partition_files = {}
partition_locks = defaultdict(threading.Lock)
master_lock = threading.Lock()

stats = defaultdict(int)
stats_lock = threading.Lock()


def get_partition_file(service, level):
    key = (service, level)

    with master_lock:

        if key not in partition_files:

            os.makedirs(PARTITION_DIR, exist_ok=True)

            filename = os.path.join(
                PARTITION_DIR,
                f"{service}_{level}.bin"
            )

            partition_files[key] = open(filename, "ab")

            print(f"Created Partition -> {filename}")

    return partition_files[key]


def encode_record(timestamp, level, service, message):

    ts = timestamp.encode("ascii").ljust(19, b" ")[:19]

    level_byte = LEVEL_CODE[level]

    service_bytes = service.encode("utf-8")
    message_bytes = message.encode("utf-8")

    header = struct.pack(
        "!19sBH",
        ts,
        level_byte,
        len(service_bytes)
    )

    msg_header = struct.pack(
        "!H",
        len(message_bytes)
    )

    return (
        header
        + service_bytes
        + msg_header
        + message_bytes
    )


def write_payload(record):

    binary = encode_record(
        record["timestamp"],
        record["level"],
        record["service"],
        record["message"]
    )

    prefix = struct.pack("!I", len(binary))

    key = (
        record["service"],
        record["level"]
    )

    file = get_partition_file(
        record["service"],
        record["level"]
    )

    with partition_locks[key]:
        file.write(prefix + binary)
        file.flush()


def process_line(line, server):

    match = LOG_PATTERN.match(line)

    if not match:

        with stats_lock:
            stats[(server, "REJECTED")] += 1

        return

    payload = {
        "timestamp": match.group("timestamp"),
        "level": match.group("level"),
        "service": match.group("service"),
        "message": match.group("message"),
    }

    write_payload(payload)

    with stats_lock:
        stats[(server, payload["level"])] += 1


def harvest(server_name, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.connect((HOST, port))

    print(f"{server_name} connected on port {port}")

    buffer = b""

    try:

        while True:

            chunk = sock.recv(4096)

            if not chunk:
                break

            buffer += chunk

            while b"\n" in buffer:

                raw, buffer = buffer.split(b"\n", 1)

                try:
                    line = raw.decode("utf-8").strip()
                except UnicodeDecodeError:
                    continue

                if line:
                    process_line(line, server_name)

    finally:
        sock.close()


def display_stats():

    while True:

        time.sleep(3)

        with stats_lock:

            if not stats:
                continue

            print("\n========== NETFLIX LIVE DASHBOARD ==========")

            for (server, level), count in sorted(stats.items()):

                print(
                    f"{server:18} {level:10} {count}"
                )

            print("============================================\n")


if __name__ == "__main__":

    threads = []

    for name, port in SERVERS:

        t = threading.Thread(
            target=harvest,
            args=(name, port),
            daemon=True
        )

        t.start()

        threads.append(t)

    dashboard = threading.Thread(
        target=display_stats,
        daemon=True
    )

    dashboard.start()

    print("\nNetflix Log Harvester Running...\n")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping Netflix Log Harvester...")

        for file in partition_files.values():
            file.close()