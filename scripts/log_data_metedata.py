import mlflow
from pathlib import Path
import pandas as pd

SPLITS_DIR = Path("data/splits")


def log_dataset_metadata(**context):
    mlflow.set_experiment("walmart_sales_week2")

    with mlflow.start_run(run_name="feature_dataset_v1"):
        for split in ["train", "val", "test"]:
            df = pd.read_parquet(SPLITS_DIR / f"{split}.parquet")
            mlflow.log_metric(f"{split}_rows", len(df))

        mlflow.log_param("feature_version", "v1")
        mlflow.log_param("split_strategy", "time_based")
        mlflow.log_param("lags", "[1,2,4]")
        mlflow.log_param("rolling_window", 4)


if __name__ == "__main__":
    log_dataset_metadata()
