import logging

from genaidrivenetl.config import Config
from genaidrivenetl.infrastructure.file_storage import strip_markdown

logger = logging.getLogger(__name__)


def generate_via_chain(state: dict, chain, required_vars: list, result_key: str, preview_label: str) -> dict:
    logger.info(f"Preparing {preview_label} inputs: {required_vars}")

    for k in required_vars:
        if k not in state:
            state[k] = getattr(Config, k.upper(), "")

    preview_str = {k: state[k] for k in required_vars}
    logger.info(f"{preview_label} with preview: {str(preview_str)[:100]}{'...' if len(preview_str) > 100 else ''}")
    invoke_input = {k: state[k] for k in required_vars}

    try:
        result = chain.invoke(invoke_input)
        state[result_key] = strip_markdown(result)
    except Exception as e:
        logger.error(f"Failed to generate {preview_label}: {e}")
        state[result_key] = ""

    return state