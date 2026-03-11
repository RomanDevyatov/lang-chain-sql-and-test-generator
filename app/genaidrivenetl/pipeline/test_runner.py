import subprocess
import logging

logger = logging.getLogger(__name__)


def run_tests(test_file="tests/generated/generated_tests.py", maxfail=1):
    """
    Run pytest on generated tests file and return dict with success and output
    """
    logger.info(f"Running tests: {test_file}")

    result = subprocess.run(
        ["pytest", test_file, "-v", f"--maxfail={maxfail}"],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr
    success = result.returncode == 0

    if not success:
        logger.warning("Tests failed:\n" + output[:500])  # preview first 500 chars

    return {"success": success, "output": output}
