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
# Run main_pipeline.py
# ==============================
#echo "Running validate_generated_sql.py..."
#./scripts/run_validate_sql.sh

# ==============================
# Run generated tests
# ==============================
echo "Running generated tests..."
./scripts/run_generated_tests.sh

# ==============================
# Run stage to prod script
# ==============================
echo "Running stage to prod..."
./scripts/run_commit_views.sh

echo "All steps finished successfully"
