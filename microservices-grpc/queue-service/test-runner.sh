#!/bin/sh
set -e

# Wait for all queue-service containers to be ready
echo "Waiting for queue-service containers to be ready..."
sleep 10

# Run the test runner script (Python)
echo "Running test suite..."
python3 /app/test_runner.py
