import subprocess
import logging

logger = logging.getLogger(__name__)

import os


def run_tests(test_file, maxfail=1):
    logger.info(f"Running tests: {test_file}")

    result = subprocess.run(
        ["poetry", "run", "pytest", test_file, "-v", f"--maxfail={maxfail}"],
        cwd="/opt/airflow",
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr
    success = result.returncode == 0

    if not success:
        logger.warning("Tests failed:\n" + output[:500])

    return {"success": success, "output": output}
