import time
from pathlib import Path

import mlflow

from genaidrivenetl.config import Config

SQL_PATH = Path(Config.GENERATED_SQL_PATH)
GEN_TEST_PATH = Path(Config.GENERATED_TESTS_PATH)


def save_sql(sql: str) -> str:
    if not sql:
        mlflow.set_tag("sql_status", "empty")
        return sql

    start = time.perf_counter()

    SQL_PATH.write_text(sql)

    mlflow.log_artifact(str(SQL_PATH), artifact_path="sql")

    mlflow.log_metric("sql_length_chars", len(sql))
    mlflow.log_metric("sql_length_lines", sql.count("\n") + 1)
    mlflow.log_metric("save_sql_latency_sec", time.perf_counter() - start)

    return sql


def read_gen_sql() -> dict:
    return SQL_PATH.read_text()


def save_raw_tests(tests: str) -> str:
    if not tests:
        mlflow.set_tag("tests_status", "empty")
        return tests

    start = time.perf_counter()

    GEN_TEST_PATH.write_text(tests)

    mlflow.log_artifact(str(GEN_TEST_PATH), artifact_path="tests")

    mlflow.log_metric("num_test_chars", len(tests))
    mlflow.log_metric("num_test_lines", tests.count("\n") + 1)
    mlflow.log_metric("save_tests_latency_sec", time.perf_counter() - start)

    return tests
