# config.py

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    # ========= PATHS =========

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUTS_DIR = DATA_DIR / "generated_outputs"
    LOG_DIR = DATA_DIR / "logs"

    PROMPTS_DIR = PROJECT_ROOT / "genaidrivenetl" / "prompts"
    GENERATED_SQL_PATH = OUTPUTS_DIR / "sql" / "etl.sql"
    GENERATED_TESTS_PATH = PROJECT_ROOT / "tests" / "generated_tests.py"

    # ========= LLM =========

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL = "arcee-ai/trinity-large-preview:free"
    OPENROUTER_BASE = "https://openrouter.ai/api/v1"

    # ========= SQL =========

    USER_METRICS_VIEW_NAME = os.getenv("VIEW_NAME")
    USER_METRICS_STAGING_VIEW_NAME = os.getenv("STAGING_VIEW_NAME")

    RAW_SCHEMA = """
    raw_events(
        user_id text,
        event_time timestamp,
        event_type text,
        session_id text,
        revenue numeric,
        user_agent text
    )
    """

    RULES = """
    - PostgreSQL compatible
    - Use GROUP BY
    - Avoid window functions
    - Include simple comments
    - Handle division by zero safely
    - Output only SQL (no markdown, no backticks)
    """

    AGGREGATES = """
    - total_revenue = sum of revenue for purchase events
    - total_events = count of all events
    - avg_revenue_per_event = total_revenue divided by total_events
    """

    REQUIRED_CHECKS = """
    - total_revenue is not null and >= 0
    - total_events > 0
    - avg_revenue_per_event >= 0
    - no duplicate user_id rows
    """

    RULES_TEST = """
    - Use only user_metrics_df fixture
    - Do not access database
    - Do not define fixtures
    - Output only plain Python code
    - No markdown, no backticks, no explanations
    """

    FIXTURE_NAME = "user_metrics_df"

    # ========= PROMPTS =========
    VERSION = "v1"
    SQL_PROMPT_PATH = PROMPTS_DIR / VERSION / "sql_prompt.txt"
    TEST_PROMPT_PATH = PROMPTS_DIR / VERSION / "test_prompt.txt"

    # ========= LOGGING =========

    LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    LOGGING_LEVEL = logging.INFO
    LOG_FILE = LOG_DIR / "app.log"

    @classmethod
    def ensure_directories(cls):
        for p in [cls.DATA_DIR, cls.OUTPUTS_DIR, cls.LOG_DIR]:
            if not p.exists():
                p.mkdir(parents=True, exist_ok=True)
