import logging

import mlflow
from dotenv import load_dotenv

from genaidrivenetl.config import Config
from genaidrivenetl.llm.factory import build_llm
from genaidrivenetl.logging_config import setup_logging
from genaidrivenetl.pipeline.pipeline import build_pipeline

logger = logging.getLogger(__name__)


load_dotenv()
Config.ensure_directories()
setup_logging()

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.langchain.autolog()


def run_pipeline():
    mlflow.set_experiment("lang-chain-mlflow-integration")

    with mlflow.start_run(run_name="genai-etl") as run:
        try:
            mlflow.log_params(
                {
                    "llm_model": Config.LLM_MODEL,
                    "sql_prompt_file": str(Config.SQL_PROMPT_PATH),
                    "test_prompt_file": str(Config.TEST_PROMPT_PATH),
                }
            )

            llm = build_llm(
                Config.LLM_MODEL,
                Config.OPENROUTER_API_KEY,
                Config.OPENROUTER_BASE,
            )

            pipeline = build_pipeline(llm)
            pipeline.invoke({})

            logger.info(f"Run ID: {run.info.run_id}")

        except Exception as e:
            logger.exception(f"Pipeline failed: {e}")

            mlflow.set_tag("run_status", "failed")
            mlflow.log_text(str(e), "error.txt")

            raise  # важно


if __name__ == "__main__":
    run_pipeline()
