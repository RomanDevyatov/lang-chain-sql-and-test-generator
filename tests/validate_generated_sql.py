import logging
import os
import sys

import sqlparse
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


SQL_PATH = "data/generated_outputs/sql/etl.sql"


def validate_syntax():
    with open(SQL_PATH) as f:
        sql = f.read()

    parsed = sqlparse.parse(sql)
    if not parsed:
        logger.info("SQL is empty or invalid")
        sys.exit(1)

    logger.info("SQL parsed successfully")

def validate_execution():
    engine = create_engine(os.getenv("DB_URL"))

    with engine.connect() as conn:
        try:
            conn.execute(text("BEGIN;"))
            conn.execute(text(open(SQL_PATH).read()))
            conn.execute(text("ROLLBACK;"))
            logger.info("SQL executes cleanly (dry run)")
        except Exception as e:
            logger.info("SQL execution failed:")
            logger.info(e)
            sys.exit(1)

if __name__ == "__main__":
    validate_syntax()
    validate_execution()
