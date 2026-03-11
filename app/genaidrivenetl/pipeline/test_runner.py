import subprocess
import logging

logger = logging.getLogger(__name__)

import os

def run_tests(
        test_file="tests/generated/generated_tests.py",
        maxfail=1, poetry_bin="/home/airflow/.local/bin/poetry",
        project_dir="/opt/airflow"
):
    env = os.environ.copy()
    env["POETRY_VIRTUALENVS_CREATE"] = "false"
    env["PATH"] = "/home/airflow/.local/bin:" + env["PATH"]

    logger.info(f"Running tests: {test_file}")

    result = subprocess.run(
        [poetry_bin, "run", "pytest", test_file, "-v", f"--maxfail={maxfail}"],
        capture_output=True,
        text=True,
        cwd=project_dir,
        env=env
    )

    output = result.stdout + result.stderr
    success = result.returncode == 0

    if not success:
        logger.warning("Tests failed:\n" + output[:500])

    return {"success": success, "output": output}