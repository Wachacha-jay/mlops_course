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

    df = pd.read_csv(INPUT_PATH)

    # Normalize and map common column names to expected names
    # e.g., Store -> store_id, Dept -> dept_id, Date -> date, Weekly_Sales -> weekly_sales
    col_lower = {c.lower().strip(): c for c in df.columns}

    def find_column(key_substrs):
        for sub in key_substrs:
            for low, orig in col_lower.items():
                if sub in low:
                    return orig
        return None

    date_col = find_column(["date"]) or "date"
    store_col = find_column(["store"]) or "store_id"
    dept_col = find_column(["dept", "department"]) or "dept_id"
    weekly_col = find_column(["weekly_sales", "weekly", "sales"]) or "weekly_sales"

    if date_col not in df.columns:
        raise ValueError(f"No date column found in input CSV; looked for: {list(col_lower.keys())}")

    # Parse date column
    df[date_col] = pd.to_datetime(df[date_col])

    # Rename to expected columns for downstream logic
    df = df.rename(columns={store_col: "store_id", dept_col: "dept_id", date_col: "date", weekly_col: "weekly_sales"})

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
