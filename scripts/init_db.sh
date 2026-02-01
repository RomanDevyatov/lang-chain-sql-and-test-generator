#!/usr/bin/env bash
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

INIT_SQL=genaidrivenetl/db/init.sql
LOAD_SQL=genaidrivenetl/db/load_data.sql

echo "Initializing database: $DB_NAME"

# ==============================
# Create DB if not exists
# ==============================

if ! psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Database $DB_NAME does not exist. Creating..."
    createdb -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" "$DB_NAME"
else
    echo "Database $DB_NAME already exists. Skipping creation."
fi

# ==============================
# Check SQL files exist
# ==============================

if [ ! -f "$INIT_SQL" ]; then
    echo "Error: $INIT_SQL not found!"
    exit 1
fi

if [ ! -f "$LOAD_SQL" ]; then
    echo "Error: $LOAD_SQL not found!"
    exit 1
fi

# ==============================
# Run init SQL
# ==============================

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f "$INIT_SQL"

# ==============================
# Load CSV data
# ==============================

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f "$LOAD_SQL"

echo "Database ready!"
