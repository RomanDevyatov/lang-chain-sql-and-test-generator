import logging
from pathlib import Path

from genaidrivenetl.config import (
    GENERATED_SQL_PATH,
    GENERATED_TESTS_PATH,
    PROMPTS_DIR,
    TEST_GENERATION_TXT,
    TRANSFORMATION_GENERATION_TXT,
)
from genaidrivenetl.llm.client import LLMClient

logger = logging.getLogger(__name__)


class ETLOrchestrator:

    def __init__(self, output_dir: Path = GENERATED_SQL_PATH):
        self.llm = LLMClient()
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_prompt(self, name: str) -> str:
        path = PROMPTS_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text()

    def generate_sql(self, raw_schema, view_name) -> Path:
        prompt = self.load_prompt(TRANSFORMATION_GENERATION_TXT).format(
            raw_schema=raw_schema,
            view_name=view_name,
        )
        logger.info(f"Sending prompt: {prompt}")

        sql = self.llm.generate(prompt)
        logger.info("Fetched response.")

        path = self.output_dir / "etl.sql"
        path.write_text(sql)
        logger.info(f"Saved generated SQL to: {path}")

        return path

    def generate_tests(self, sql_logic, view_name, fixture_name) -> Path:
        prompt = self.load_prompt(TEST_GENERATION_TXT).format(
            sql_logic=sql_logic, view_name=view_name, fixture_name=fixture_name
        )

        logger.info(f"Sending test prompt: {prompt}")
        tests = self.llm.generate(prompt)
        logger.info("Fetched response.")

        path = GENERATED_TESTS_PATH
        path.write_text(tests)
        logger.info(f"Saved generated tests to: {path}")

        return path
