#!/usr/bin/env bash
set -e

# ==============================
# Load env variables
# ==============================

# set -a
# source .env
# set +a

# ==============================
# Run generated tests
# ==============================

# POETRY_BIN=/home/airflow/.local/bin/poetry
: "${POETRY_BIN:?Need POETRY_BIN}"

PROJECT_DIR=/opt/airflow
TEST_FILE=$PROJECT_DIR/tests/generated/generated_tests.py

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: $TEST_FILE not found! Please generate tests first."
    exit 1
fi

export PATH="/home/airflow/.local/bin:$PATH"

export POETRY_VIRTUALENVS_CREATE=false

echo "Running generated tests: $TEST_FILE"
cd $PROJECT_DIR

"$POETRY_BIN" run pytest -v "$TEST_FILE"

echo "Generated tests completed successfully"
