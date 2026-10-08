"""
Pre-packaged Example Architecture and Code Scenarios for GemmaLens Demos
Author: Shasank Paruchuri (paruchurishasank04@gmail.com)
License: Apache-2.0
"""

SAMPLE_ARCHITECTURES = {
    "e_commerce_monolith": {
        "title": "Single-Database E-Commerce Checkout",
        "description": "User -> Single Load Balancer -> 1 Web App Server -> 1 Primary PostgreSQL Database (No read replicas, no cache).",
        "known_issues": ["Single Point of Failure at DB", "No Redis session caching", "No async payment processing queue"]
    },
    "iot_telemetry_pipeline": {
        "title": "High-Throughput IoT Ingestion",
        "description": "50,000 IoT Sensors -> REST Ingest API -> Direct SQL Writes -> Dashboard Polling.",
        "known_issues": ["Direct DB write starvation under peak load", "Missing Kafka / RabbitMQ buffer", "Missing time-series aggregation"]
    }
}

SAMPLE_CODE_SNIPPETS = {
    "c_pointer_leak": {
        "language": "C",
        "filename": "examples/c_memory_bug.c",
        "highlight": "Buffer overflow in array write loop, dangling stack pointer, and unfreed heap memory."
    }
}
