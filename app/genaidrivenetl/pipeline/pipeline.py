import logging

from langchain_core.runnables import RunnableLambda

from genaidrivenetl.config import Config
from genaidrivenetl.infrastructure.file_storage import (
    save_raw_tests,
    save_sql,
    strip_markdown,
)
from genaidrivenetl.pipeline.chains import build_chain
from genaidrivenetl.pipeline.inputs import (
    prepare_gen_sql_inputs,
    prepare_gen_test_inputs,
)

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
    result = chain.invoke(state)
    state["sql"] = strip_markdown(result)
    return state


def generate_tests(state, chain):
    result = chain.invoke(state)
    state["tests"] = strip_markdown(result)
    return state


def evaluate_sql_step(state: dict, chain) -> dict:
    sql = state.get("sql", "")
    state["sql_score"] = chain.invoke({"sql": sql, **state})
    return state


def build_pipeline(llm):
    gen_sql_chain = build_chain(llm, Config.SQL_PROMPT_PATH)
    gen_test_chain = build_chain(llm, Config.TEST_PROMPT_PATH)
    fix_chain = build_chain(llm, Config.FIX_PIPELINE_PROMPT_PATH)
    evaluate_chain = build_chain(llm, Config.FIX_PIPELINE_PROMPT_PATH)

    return (
        log_with_preview("Preparing gen SQL inputs...")
        | RunnableLambda(prepare_gen_sql_inputs)
        | log_with_preview("Generating SQL...")
        | RunnableLambda(lambda state: generate_sql(state, gen_sql_chain))
        | log_with_preview("Saving SQL to disk...")
        | RunnableLambda(save_sql)
        | log_with_preview("Evaluating SQL...")
        | RunnableLambda(lambda state: evaluate_sql(state, evaluate_chain))
        | log_with_preview("Preparing gen test inputs...")
        | RunnableLambda(prepare_gen_test_inputs)
        | log_with_preview("Generating tests...")
        | RunnableLambda(lambda state: generate_tests(state, gen_test_chain))
        | log_with_preview("Saving tests to disk...")
        | RunnableLambda(save_raw_tests)
        | log_with_preview("Running feedback loop...")
        | RunnableLambda(lambda state: universal_feedback_loop(state, fix_chain))
    )
