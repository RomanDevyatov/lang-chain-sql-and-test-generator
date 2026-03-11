import json
import logging

from .test_runner import run_tests
from ..config import Config
from ..infrastructure.file_storage import save_sql, save_raw_tests


MAX_RETRIES = 3


logger = logging.getLogger(__name__)


def universal_feedback_loop(state, fix_chain):

    for attempt in range(MAX_RETRIES):

        result = run_tests("tests/generated/generated_tests.py")

        if result["success"]:
            logger.info("Tests passed!")
            return state

        logger.error(f"Attempt {attempt + 1} failed. Output:\n{result['output']}")
        logger.info("Asking LLM to fix...")

        sql = Config.GENERATED_SQL_PATH.read_text()
        tests = Config.GENERATED_TESTS_PATH.read_text()

        fix = fix_chain.invoke({
            "sql": sql,
            "tests": tests,
            "error": result["output"]
        })

        fix_json = json.loads(fix)

        save_sql(fix_json["sql"])
        save_raw_tests(fix_json["tests"])

    raise RuntimeError("Pipeline could not be fixed")