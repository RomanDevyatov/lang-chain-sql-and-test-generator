from genaidrivenetl.config import Config

import logging
import mlflow

logger = logging.getLogger(__name__)


def evaluate_sql(state, chain):
    """Evaluates generated SQL and assigns a score (0-10)."""
    evaluate_input = {
        "sql": state.get("sql", ""),
        "raw_schema": state.get("raw_schema", Config.RAW_SCHEMA),
        "business_rules": state.get("rules", Config.RULES),
    }

    score_str = chain.invoke(evaluate_input)

    try:
        score = int(score_str.strip())
        if score < 0:
            score = 0
        elif score > 10:
            score = 10
    except Exception as e:
            logger.error(f"Error evaluating SQL: {e}. Assigning fallback score 0.")
            score = 0

    mlflow.log_metric("sql_score", score)

    logger.info(f"SQL evaluation score: {score}/10")

    state["sql_score"] = score

    return state
