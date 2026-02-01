#!/usr/bin/env bash
set -e

# ==============================
# Load env variables
# ==============================

set -a
source .env
set +a

# ==============================
# Run generated tests
# ==============================

TEST_FILE=tests/generated_tests.py

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: $TEST_FILE not found! Please generate tests first."
    exit 1
fi

echo "Running generated tests: $TEST_FILE"

poetry run pytest -v "$TEST_FILE"

echo "Generated tests completed successfully"
