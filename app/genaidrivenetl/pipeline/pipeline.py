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

logger = logging.getLogger(__file__)


def log_with_preview(message: str):
    def _log(x):
        logger.info(
            f"{message} | Preview: {str(x)[:100]}{'...' if len(str(x)) > 100 else ''}"
        )
        return x

    return RunnableLambda(_log)


def build_pipeline(llm):
    gen_sql_chain = build_chain(llm, Config.SQL_PROMPT_PATH)
    gen_test_chain = build_chain(llm, Config.TEST_PROMPT_PATH)

    return (
        log_with_preview("Preparing gen SQL inputs...")
        | RunnableLambda(prepare_gen_sql_inputs)
        | log_with_preview("Generating SQL...")
        | gen_sql_chain
        | RunnableLambda(strip_markdown)
        | log_with_preview("Saving SQL to disk...")
        | RunnableLambda(save_sql)
        | log_with_preview("Preparing gen test inputs...")
        | RunnableLambda(prepare_gen_test_inputs)
        | log_with_preview("Generating tests...")
        | gen_test_chain
        | RunnableLambda(strip_markdown)
        | log_with_preview("Saving tests to disk...")
        | RunnableLambda(save_raw_tests)
    )
