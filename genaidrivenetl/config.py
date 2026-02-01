from pathlib import Path
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# ========= PROJECT ROOT =========

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENAI_ROOT = PROJECT_ROOT / "genaidrivenetl"

DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = DATA_DIR / "generated_outputs"
LOG_DIR = DATA_DIR / "logs"

for p in [DATA_DIR, OUTPUTS_DIR, LOG_DIR]:
    p.mkdir(parents=True, exist_ok=True)

PROMPTS_DIR = GENAI_ROOT / "prompts"

GENERATED_SQL_PATH = OUTPUTS_DIR / "sql"
TESTS_DIR = PROJECT_ROOT / "tests"
GENERATED_TESTS_PATH = TESTS_DIR / "generated_tests.py"

TRANSFORMATION_GENERATION_TXT = "transformation_generation.txt"
TEST_GENERATION_TXT = "test_generation.txt"

# ========= LLM =========

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

LLM_MODELS = [
    "arcee-ai/trinity-large-preview:free",
]

logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"GENAI_ROOT: {GENAI_ROOT}")
logger.info(f"OUTPUTS_DIR: {OUTPUTS_DIR}")
logger.info(f"PROMPTS_DIR: {PROMPTS_DIR}")
logger.info(f"DATA_DIR: {DATA_DIR}")
logger.info(f"GENERATED_SQL_PATH: {GENERATED_SQL_PATH}")
logger.info(f"GENERATED_TESTS_PATH: {GENERATED_TESTS_PATH}")
logger.info(f"LLM_MODELS: {LLM_MODELS}")

# ========= LOG ==========
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_FILE = LOG_DIR / "app.log"
LOGGING_LEVEL = logging.INFO