from genaidrivenetl.config import Config


def prepare_gen_sql_inputs(state: dict) -> dict:
    return {
        **state,
        "raw_schema": state.get("raw_schema", Config.RAW_SCHEMA),
        "view_name": state.get("view_name", Config.STAGING_VIEW_NAME),
        "rules": state.get("rules", Config.RULES),
        "aggregates": state.get("aggregates", Config.AGGREGATES),
    }


def prepare_gen_test_inputs(state: dict) -> dict:
    return {
        **state,
        "sql": state.get("sql", ""),
        "view_name": state.get("view_name", Config.VIEW_NAME),
        "fixture_name": state.get("fixture_name", Config.FIXTURE_NAME),
        "required_checks": state.get("required_checks", Config.REQUIRED_CHECKS),
        "rules_test": state.get("rules_test", Config.RULES_TEST),
    }
