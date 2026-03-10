#!/usr/bin/env bash
set -e

PROJECT_DIR=/opt/airflow
POETRY_BIN=/home/airflow/.local/bin/poetry
TEST_FILE=$PROJECT_DIR/tests/generated/generated_tests.py

export PATH="/home/airflow/.local/bin:$PATH"

cd $PROJECT_DIR

echo "Running Black (autoformat)..."
$POETRY_BIN run black genaidrivenetl "$TEST_FILE"

echo "Running isort (import sort)..."
$POETRY_BIN run isort genaidrivenetl "$TEST_FILE"

# echo "Running Flake8 (PEP8 checks)..."
# $POETRY_BIN run flake8 genaidrivenetl "$TEST_FILE"

echo "Linting and formatting complete!"
