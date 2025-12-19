# scripts/download_data.py

import shutil
from pathlib import Path
import logging
import zipfile

RAW_DATA_DIR = Path("data/raw")
SOURCE_FILE = Path("data/source/sales.csv")  # temporary/manual drop location
TARGET_FILE = RAW_DATA_DIR / "sales.csv"
ZIP_FILE = Path("../data/walmart_archive.zip")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def unzip_sales_data():
    """
    Unzips the sales file from the archive if it exists and hasn't been extracted yet.
    """
    if ZIP_FILE.exists():
        logger.info("Unzipping sales data from %s", ZIP_FILE)
        target_dir = Path("data/source")
        target_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(path=target_dir)
        logger.info("Sales data unzipped to %s", target_dir)
    else:
        logger.warning("Zip file not found at %s", ZIP_FILE)


def download_data(**context):
    """
    Stages raw Walmart sales data into the pipeline.

    This function is intentionally idempotent:
    - If the file already exists, it will NOT overwrite it.
    - Prevents accidental data mutation.
    """

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if TARGET_FILE.exists():
        logger.info("Raw data already exists. Skipping ingestion.")
        return str(TARGET_FILE)

    source_file = SOURCE_FILE
    if not source_file.exists():
        alt = Path("data/source/train.csv")
        if alt.exists():
            logger.info("Found alternative source file %s", alt)
            source_file = alt
        else:
            raise FileNotFoundError(
                f"Source file not found at {SOURCE_FILE}. "
                "Place the Kaggle CSV here before running the DAG."
            )

    shutil.copy2(source_file, TARGET_FILE)

    logger.info("Raw data copied to %s", TARGET_FILE)

    return str(TARGET_FILE)


if __name__ == "__main__":
    unzip_sales_data()
    download_data()
