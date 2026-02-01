#!/usr/bin/env bash
set -e

# ==============================
# Load environment variables
# ==============================
set -a
source .env
set +a

# ==============================
# Run DB initialization
# ==============================
echo "Running init_db.sh..."
./scripts/init_db.sh

# ==============================
# Run main_pipeline.py
# ==============================
echo "Running main_pipeline.py..."
./scripts/run_main_pipeline.sh

# ==============================
# Run generated tests
# ==============================
echo "Running generated tests..."
./scripts/run_generated_tests.sh

echo "All steps finished successfully"
