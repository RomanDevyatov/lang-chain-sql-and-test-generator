import logging
from pathlib import Path
from genaidrivenetl.llm.client import LLMClient

from genaidrivenetl.config import (
    PROMPTS_DIR, GENERATED_SQL_PATH, GENERATED_TESTS_PATH, TRANSFORMATION_GENERATION_TXT, TEST_GENERATION_TXT,
)


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

    def generate_sql(self, raw_schema, rules) -> Path:
        prompt = self.load_prompt(TRANSFORMATION_GENERATION_TXT).format(
            raw_schema=raw_schema,
            business_rules=rules
        )
        logger.info(f'Sending prompt: {prompt}')

        sql = self.llm.generate(prompt)
        logger.info(f'Fetched response.')

        path = self.output_dir / "etl.sql"
        path.write_text(sql)
        logger.info(f'Saved generated SQL to: {path}')

        return path

    def generate_tests(self, sql_logic) -> Path:
        prompt = self.load_prompt(TEST_GENERATION_TXT).format(
            sql_logic=sql_logic
        )

        logger.info(f'Sending test prompt.')
        tests = self.llm.generate(prompt)
        logger.info(f'Fetched response.')

        path = GENERATED_TESTS_PATH
        path.write_text(tests)
        logger.info(f"Saved generated tests to: {path}")

        return path
