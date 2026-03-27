import json
import logging

from ..config import Config
from ..infrastructure.file_storage import save_raw_tests, save_sql
from .test_runner import run_tests
from .evaluate import evaluate_sql

MAX_RETRIES = 3


logger = logging.getLogger(__name__)


def universal_feedback_loop(state: dict, fix_chain, evaluate_chain, score_threshold: int = 8):

    for attempt in range(MAX_RETRIES):

        result = run_tests("tests/generated/generated_tests.py")

        if result["success"]:
            logger.info("Tests passed!")
            return state

        logger.error(f"Attempt {attempt + 1} failed. Output:\n{result['output']}")
        logger.info("Asking LLM to fix...")

        sql = Config.GENERATED_SQL_PATH.read_text()
        tests = Config.GENERATED_TESTS_PATH.read_text()

        fix = fix_chain.invoke({"sql": sql, "tests": tests, "error": result["output"]})

        fix_json = json.loads(fix)

        save_sql(fix_json["sql"])
        save_raw_tests(fix_json["tests"])

        state.update({
            "sql": fix_json["sql"],
            "tests": fix_json["tests"]
        })

        state = evaluate_sql_step(state, evaluate_chain)
        logger.info(f"SQL score after fix: {state['sql_score']}")

        if state["sql_score"] >= score_threshold:
            logger.info(f"SQL score above threshold ({score_threshold}), rerunning tests...")
        else:
            logger.warning(f"SQL score below threshold ({score_threshold}), continuing feedback loop...")

    raise RuntimeError("Pipeline could not be fixed")
