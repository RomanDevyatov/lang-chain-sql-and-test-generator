#!/usr/bin/env bash
set -euo pipefail

echo "Promoting staging view to production."

: "${DB_USER:?Need DB_USER}"
: "${DB_HOST:?Need DB_HOST}"
: "${DB_PORT:?Need DB_PORT}"
: "${DB_NAME:?Need DB_NAME}"
: "${VIEW_NAME:?Need VIEW_NAME}"
: "${STAGING_VIEW_NAME:?Need STAGING_VIEW_NAME}"

export PGPASSWORD=$DB_PASSWORD

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" <<EOF
BEGIN;

DROP VIEW IF EXISTS $VIEW_NAME;
ALTER VIEW $STAGING_VIEW_NAME RENAME TO $VIEW_NAME;

COMMIT;
EOF

echo "View promoted successfully"
