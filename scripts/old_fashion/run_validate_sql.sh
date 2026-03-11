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

TEST_FILE=tests/validate_generated_sql.py

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: $TEST_FILE not found! Please add validate sql test first."
    exit 1
fi

echo "Validating tests: $TEST_FILE"

poetry run pytest -v "$TEST_FILE"

echo "Generated sql tested successfully"
