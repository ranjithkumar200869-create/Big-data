"""
read_binary_logs.py
--------------------
Reads back one binary partition file and decodes it into
human-readable Netflix service logs.

This demonstrates that the .bin files contain structured,
recoverable Netflix log records.

Usage:
    python read_binary_logs.py partitions/netflix_ERROR.bin
"""

import struct
import sys

LEVEL_CODE = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3
}

CODE_LEVEL = {v: k for k, v in LEVEL_CODE.items()}


def read_records(filepath):
    """Read and decode binary Netflix log records."""

    with open(filepath, "rb") as file:
        data = file.read()

    records = []
    offset = 0

    while offset < len(data):

        # Read record length (4 bytes)
        (record_length,) = struct.unpack_from("!I", data, offset)
        offset += 4

        # Extract one complete record
        record = data[offset:offset + record_length]
        offset += record_length

        # Decode header
        timestamp, level_code, service_length = struct.unpack_from(
            "!19sBH", record, 0
        )

        position = 22

        service = record[position:position + service_length].decode("utf-8")
        position += service_length

        (message_length,) = struct.unpack_from("!H", record, position)
        position += 2

        message = record[position:position + message_length].decode("utf-8")

        records.append({
            "timestamp": timestamp.decode("ascii").strip(),
            "level": CODE_LEVEL.get(level_code, "UNKNOWN"),
            "service": service,
            "message": message
        })

    return records


def print_logs(records):
    """Display Netflix log records."""

    print("\n========== NETFLIX LOG REPORT ==========\n")

    for record in records:
        print(
            f"[{record['timestamp']}] "
            f"{record['level']:8} | "
            f"{record['service']:20} | "
            f"{record['message']}"
        )

    print("\n========================================")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python read_binary_logs.py partitions/netflix_ERROR.bin")
        sys.exit(1)

    filepath = sys.argv[1]

    logs = read_records(filepath)

    print(f"\nTotal Records Found: {len(logs)}")
    print_logs(logs)