import pandas as pd
from pathlib import Path
import logging

INPUT_PATH = Path("data/validated/sales_validated.csv")
OUTPUT_PATH = Path("data/features/sales_features.parquet")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_features(**context):
    if not INPUT_PATH.exists():
        raise FileNotFoundError("Validated data not found")

    df = pd.read_csv(INPUT_PATH, parse_dates=["date"])

    df = df.sort_values(["store_id", "dept_id", "date"])

    # Time features
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["year"] = df["date"].dt.year

    # Lag features
    for lag in [1, 2, 4]:
        df[f"sales_lag_{lag}"] = (
            df.groupby(["store_id", "dept_id"])["weekly_sales"]
              .shift(lag)
        )

    # Rolling features
    df["sales_roll_mean_4"] = (
        df.groupby(["store_id", "dept_id"])["weekly_sales"]
          .shift(1)
          .rolling(4)
          .mean()
    )

    df = df.dropna().reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH)

    logger.info("Feature dataset written to %s", OUTPUT_PATH)
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    generate_features()
