#!/usr/bin/env bash
set -e

echo "Promoting staging view to production."

DB_URL="$DB_URL"
VIEW_NAME="$VIEW_NAME"
STAGING_VIEW_NAME="$STAGING_VIEW_NAME"

psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" <<EOF
DROP VIEW IF EXISTS $VIEW_NAME;
ALTER VIEW $STAGING_VIEW_NAME RENAME TO $VIEW_NAME;
EOF

echo "View promoted successfully"
