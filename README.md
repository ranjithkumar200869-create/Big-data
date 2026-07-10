Netflix Distributed Log Collection System
Project Overview

The Netflix Distributed Log Collection System is a Python-based distributed logging application that simulates multiple Netflix regional servers generating streaming logs in real time.

The project demonstrates how distributed systems collect, validate, partition, store, and retrieve log data efficiently using TCP socket programming, multithreading, regular expressions, and binary file storage.

Objectives
Simulate multiple Netflix regional servers.
Collect logs from different servers simultaneously.
Validate incoming log records using Regular Expressions.
Store logs in compact binary format.
Partition logs dynamically based on server and severity level.
Decode binary files back into readable log records.
Technologies Used
Python 3.x
Socket Programming (TCP)
Multithreading
Regular Expressions (Regex)
Binary File Handling
Struct Module
OS Module
Project Structure
Netflix-Distributed-Log-System/

│
├── server.py
├── harvester.py
├── read_binary.py
│
├── partitions/
│   ├── netflix-india_INFO.bin
│   ├── netflix-india_ERROR.bin
│   ├── netflix-usa_WARNING.bin
│   ├── netflix-europe_DEBUG.bin
│   └── ...
│
└── README.md
Features
Simulates three Netflix regional servers.
Generates streaming logs continuously.
Uses TCP sockets for communication.
Supports multithreaded log collection.
Validates logs using Regex.
Rejects corrupted log records.
Creates partition files automatically.
Stores logs in compact binary format.
Reads binary logs back into readable text.
Simulated Netflix Servers
Server	Port
netflix-india	9001
netflix-usa	9002
netflix-europe	9003
Log Format

Each generated log follows this format:

YYYY-MM-DD HH:MM:SS | LEVEL | SERVER | MESSAGE

Example:

2026-07-10 11:25:40 | INFO | netflix-india | Movie#315 playback started
Workflow
Step 1

Run the Netflix server simulator.

python server.py

The simulator starts three regional servers that continuously generate log data.

Step 2

Run the log harvester.

python harvester.py

The harvester:

Connects to all Netflix servers
Reads TCP log streams
Validates logs using Regex
Rejects invalid logs
Converts logs into structured records
Stores them into binary partition files
Step 3

Read any binary partition file.

Example:

python read_binary.py partitions/netflix-india_INFO.bin

The binary records are decoded and displayed as readable logs.

Binary Record Format

Each log record is stored in binary format using the following layout:

Field	Size
Timestamp	19 Bytes
Log Level	1 Byte
Service Name Length	2 Bytes
Service Name	Variable
Message Length	2 Bytes
Message	Variable

Each record is also prefixed with a 4-byte length field to simplify decoding.

Dynamic Partitioning

Logs are automatically stored into different binary files based on:

Server Name
Log Level

Examples:

netflix-india_INFO.bin

netflix-india_ERROR.bin

netflix-usa_WARNING.bin

netflix-europe_DEBUG.bin
Sample Output
========== NETFLIX LIVE DASHBOARD ==========

netflix-india      INFO        150
netflix-india      ERROR        18
netflix-usa        WARNING      25
netflix-europe     DEBUG        61

===========================================

Decoded binary logs:

[2026-07-10 11:20:10] INFO     | netflix-india      | User#1456 logged in successfully

[2026-07-10 11:20:12] ERROR    | netflix-usa        | Playback failed for Movie#512

[2026-07-10 11:20:15] WARNING  | netflix-europe     | Buffering detected during Movie#305
Applications
Distributed Log Management
Streaming Platform Monitoring
Cloud Computing
Microservices Logging
Event Processing Systems
Real-Time Log Analytics
Future Enhancements
Store logs in a database (MySQL or MongoDB)
Build a real-time monitoring dashboard
Add log compression
Encrypt binary log files
Integrate with Apache Kafka
Add data visualization and analytics
