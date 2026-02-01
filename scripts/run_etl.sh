#!/bin/bash
set -e

# ==============================
# Load env variables
# ==============================

set -a
source .env
set +a

# ==============================
# Paths
# ==============================

ETL_SQL=data/generated_outputs/sql/etl.sql

echo "Running ETL SQL on database: $DB_NAME"

# ==============================
# Check ETL SQL file exists
# ==============================

if [ ! -f "$ETL_SQL" ]; then
    echo "Error: $ETL_SQL not found. Please generate ETL SQL first."
    exit 1
fi

# ==============================
# Execute ETL SQL
# ==============================

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f "$ETL_SQL"

echo "ETL SQL executed successfully"
