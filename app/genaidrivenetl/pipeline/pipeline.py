import logging

from langchain_core.runnables import RunnableLambda

from genaidrivenetl.config import Config
from genaidrivenetl.infrastructure.file_storage import (
    save_raw_tests,
    save_sql,
    strip_markdown,
)
from genaidrivenetl.pipeline.chains import build_chain

from .evaluate import evaluate_sql
from .feedback import universal_feedback_loop

logger = logging.getLogger(__file__)


def log_with_preview(message: str):
    def _log(x):
        logger.info(
            f"{message} | Preview: {str(x)[:100]}{'...' if len(str(x)) > 100 else ''}"
        )
        return x

    return RunnableLambda(_log)


def generate_sql(state, chain):
    return generate_via_chain(
        state,
        chain,
        required_vars=["raw_schema", "view_name", "rules", "aggregates"],
        result_key="sql",
        preview_label="SQL generation"
    )


def generate_tests(state, chain):
    return generate_via_chain(
        state,
        chain,
        required_vars=["sql", "view_name", "fixture_name", "required_checks", "rules_test"],
        result_key="tests",
        preview_label="Test generation"
    )


def build_pipeline(llm):
    gen_sql_chain = build_chain(llm, Config.SQL_PROMPT_PATH)
    gen_test_chain = build_chain(llm, Config.TEST_PROMPT_PATH)    
    evaluate_chain = build_chain(llm, Config.EVALUATE_PROMPT_PATH)
    fix_chain = build_chain(llm, Config.FIX_PIPELINE_PROMPT_PATH)

    return (
        log_with_preview("Generating SQL...")
        | RunnableLambda(lambda state: generate_sql(state, gen_sql_chain))
        | log_with_preview("Saving SQL to disk...")
        | RunnableLambda(save_sql)
        | log_with_preview("Evaluating SQL...")
        | RunnableLambda(lambda state: evaluate_sql(state, evaluate_chain))
        | log_with_preview("Generating tests...")
        | RunnableLambda(lambda state: generate_tests(state, gen_test_chain))
        | log_with_preview("Saving tests to disk...")
        | RunnableLambda(save_raw_tests)
        | log_with_preview("Running feedback loop...")
        | RunnableLambda(lambda state: universal_feedback_loop(state, fix_chain, evaluate_chain))
    )
