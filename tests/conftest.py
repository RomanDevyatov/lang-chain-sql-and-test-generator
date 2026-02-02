import logging
import os

import pandas as pd
import pytest
from sqlalchemy import create_engine, text

from genaidrivenetl.config import USER_METRICS_STAGING_VIEW_NAME, USER_METRICS_VIEW_NAME

logger = logging.getLogger(__name__)


ETL_SQL_PATH = "data/generated_outputs/sql/etl.sql"


# =========================
# SQLAlchemy engine
# =========================

@pytest.fixture(scope="session")
def engine():
    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)
    yield engine
    engine.dispose()


# =========================
# Run ETL once per session
# =========================

@pytest.fixture(scope="session")
def run_etl(engine):
    validate_etl_sql(engine, ETL_SQL_PATH)
    execute_etl(engine, ETL_SQL_PATH)
    logger.info(f"ETL SQL completed — view {USER_METRICS_VIEW_NAME} created")
    return engine


# =========================
# Execute ETL
# =========================

def execute_etl(engine, etl_sql_path):
    with open(etl_sql_path) as f:
        sql = f.read()
    with engine.begin() as conn:
        conn.execute(text(sql))


# =========================
# Validate generated ETL
# =========================

def validate_etl_sql(engine, etl_sql_path):
    if not os.path.isfile(etl_sql_path):
        raise FileNotFoundError(f"{etl_sql_path} not found")

    with open(etl_sql_path) as f:
        sql = f.read()

    with engine.begin() as conn:
        try:
            conn.execute(text(f"BEGIN; {sql}; ROLLBACK;"))
        except Exception as e:
            raise RuntimeError(f"Error in SQL {etl_sql_path}: {e}")


# =========================
# Load ETL result
# =========================

@pytest.fixture(scope="session")
def user_metrics_df(run_etl):
    return pd.read_sql(
        f"SELECT * FROM {USER_METRICS_STAGING_VIEW_NAME} ORDER BY user_id",
        run_etl
    )
