import logging

from genaidrivenetl.config import RAW_SCHEMA, USER_METRICS_VIEW_NAME, FIXTURE_NAME, USER_METRICS_STAGING_VIEW_NAME
from llm.orchestrator import ETLOrchestrator

from dotenv import load_dotenv
from genaidrivenetl.logging_config import setup_logging


logger = logging.getLogger(__name__)

# RAW_SCHEMA = """
# raw_events(
#  user_id text,
#  event_time timestamp,
#  event_type text,
#  session_id text,
#  revenue numeric,
#  user_agent text
# )
# """


load_dotenv()
setup_logging()


def main():
    orchestrator = ETLOrchestrator()
    generated_sql_file_path = orchestrator.generate_sql(RAW_SCHEMA, USER_METRICS_STAGING_VIEW_NAME)

    sql_logic = generated_sql_file_path.read_text()
    orchestrator.generate_tests(sql_logic, USER_METRICS_STAGING_VIEW_NAME, FIXTURE_NAME)

if __name__ == "__main__":
    main()
