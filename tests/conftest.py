import os
import logging
import pytest
import pandas as pd
from sqlalchemy import create_engine, text


logger = logging.getLogger(__name__)


ETL_SQL_PATH = "data/generated_outputs/sql/etl.sql"


@pytest.fixture(scope="session")
def session_metrics_df():
    if not os.path.isfile(ETL_SQL_PATH):
        raise FileNotFoundError(f"{ETL_SQL_PATH} not found. Generate ETL SQL first.")

    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)

    with open(ETL_SQL_PATH, "r") as f:
        sql_content = f.read()

    with engine.begin() as conn:
        df = pd.read_sql(text(sql_content), conn)

    logger.info(f"ETL SQL executed and session_metrics loaded: {ETL_SQL_PATH}")
    return df
