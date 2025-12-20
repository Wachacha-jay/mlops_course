import pandas as pd
from pathlib import Path
import logging

FEATURES_PATH = Path("data/features/sales_features.parquet")
SPLITS_DIR = Path("data/splits")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_data(**context):
    df = pd.read_parquet(FEATURES_PATH)
    df = df.sort_values("date")

    n = len(df)
    train_end = int(0.7 * n)
    val_end = int(0.85 * n)

    train = df.iloc[:train_end]
    val = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]

    SPLITS_DIR.mkdir(parents=True, exist_ok=True)

    train.to_parquet(SPLITS_DIR / "train.parquet")
    val.to_parquet(SPLITS_DIR / "val.parquet")
    test.to_parquet(SPLITS_DIR / "test.parquet")

    logger.info("Data splits created: train=%d val=%d test=%d",
                len(train), len(val), len(test))

    return {
        "train_rows": len(train),
        "val_rows": len(val),
        "test_rows": len(test)
    }


if __name__ == "__main__":
    split_data()
