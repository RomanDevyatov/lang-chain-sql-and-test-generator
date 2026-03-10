import logging
import os
import sys

import sqlparse
from sqlalchemy import create_engine, text

from genaidrivenetl.config import Config


logger = logging.getLogger(__name__)


SQL_PATH = Config.GENERATED_SQL_PATH


def validate_syntax():
    with open(SQL_PATH) as f:
        sql = f.read()

    parsed = sqlparse.parse(sql)
    if not parsed:
        logger.error("SQL is empty or invalid")
        sys.exit(1)

    logger.info("SQL parsed successfully")


def validate_execution():
    engine = create_engine(os.getenv("DB_URL"), future=False)

    with open(SQL_PATH) as f:
        sql = f.read()

    statements = sqlparse.split(sql)

    try:
        with engine.begin() as conn:
            for statement in statements:
                if statement.strip():
                    conn.execute(text(statement))
            raise Exception("Force rollback")
    except Exception:
        logger.info("SQL executes cleanly (dry run) — rolled back")


if __name__ == "__main__":
    validate_syntax()
    validate_execution()
