# scripts/persist_data.py

import shutil
import subprocess
from pathlib import Path
import logging

RAW_DATA_PATH = Path("data/raw/sales.csv")
VALIDATED_DATA_DIR = Path("data/validated")
VALIDATED_DATA_PATH = VALIDATED_DATA_DIR / "sales_validated.csv"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def persist_validated_data(**context):
    """
    Persists validated data and snapshots it with DVC.

    This step assumes validation has already passed.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Validated source not found at {RAW_DATA_PATH}. "
            "Validation must run before persistence."
        )

    VALIDATED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Overwrite is allowed here because this is a derived artifact
    shutil.copy2(RAW_DATA_PATH, VALIDATED_DATA_PATH)

    logger.info("Validated data written to %s", VALIDATED_DATA_PATH)

    # Track with DVC
    run_cmd(["dvc", "add", str(VALIDATED_DATA_PATH)])
    run_cmd(["git", "add", f"{VALIDATED_DATA_PATH}.dvc"])
    run_cmd(
        ["git", "commit", "-m", "Snapshot validated Walmart sales data (Week 1)"],
        allow_fail=True,  # commit may be empty on re-runs
    )

    logger.info("Validated data snapshot committed successfully")

    return str(VALIDATED_DATA_PATH)


def run_cmd(cmd, allow_fail=False):
    """
    Utility to run shell commands safely.
    """
    logger.info("Running command: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(result.stderr)
        if not allow_fail:
            raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    else:
        logger.info(result.stdout)


if __name__ == "__main__":
    persist_validated_data()
