from genaidrivenetl.config import Config


def prepare_gen_sql_inputs(_: dict) -> dict:
    return {
        "raw_schema": Config.RAW_SCHEMA,
        "view_name": Config.USER_METRICS_STAGING_VIEW_NAME,
        "rules": Config.RULES,
        "aggregates": Config.AGGREGATES,
    }


def prepare_gen_test_inputs(sql: str) -> dict:
    return {
        "sql_logic": sql,
        "view_name": Config.USER_METRICS_VIEW_NAME,
        "fixture_name": Config.FIXTURE_NAME,
        "required_checks": Config.REQUIRED_CHECKS,
        "rules_test": Config.RULES_TEST,
    }
