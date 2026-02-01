import logging
from llm.orchestrator import ETLOrchestrator

from dotenv import load_dotenv
from genaidrivenetl.logging_config import setup_logging


logger = logging.getLogger(__name__)

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

BUSINESS_RULES = """
Create sessions after 30 minutes inactivity.
Exclude bots.
Revenue only from purchase events.
"""


load_dotenv()
setup_logging()


def main():
    orchestrator = ETLOrchestrator()
    generated_sql_file_path = orchestrator.generate_sql(RAW_SCHEMA, BUSINESS_RULES)

    sql_logic = generated_sql_file_path.read_text()
    orchestrator.generate_tests(sql_logic)

if __name__ == "__main__":
    main()
