#!/usr/bin/env bash
set -e

# ==============================
# Load environment variables
# ==============================
set -a
source .env
set +a

# ==============================
# Ensure Poetry dependencies are installed
# ==============================
poetry install --no-root

# ==============================
# Run main ETL pipeline
# ==============================
echo "Running main_pipeline.py..."
poetry run python genaidrivenetl/run_pipeline.py

echo "run_pipeline.py finished successfully"
