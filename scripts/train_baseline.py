import mlflow
import pandas as pd
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

DATA_DIR = Path("data/splits")


def train_baseline(**context):
    train = pd.read_parquet(DATA_DIR / "train.parquet")
    val = pd.read_parquet(DATA_DIR / "val.parquet")

    target = "weekly_sales"
    features = [c for c in train.columns if c not in ["date", target]]

    X_train, y_train = train[features], train[target]
    X_val, y_val = val[features], val[target]

    mlflow.set_experiment("walmart_week3_baselines")

    with mlflow.start_run(run_name="ridge_baseline"):
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        preds = model.predict(X_val)

        mae = mean_absolute_error(y_val, preds)
        rmse = np.sqrt(mean_squared_error(y_val, preds))

        mlflow.log_metric("val_mae", mae)
        mlflow.log_metric("val_rmse", rmse)
        mlflow.log_param("model_type", "ridge")
        mlflow.log_param("alpha", 1.0)

        mlflow.sklearn.log_model(model, "model")

    return {"mae": mae, "rmse": rmse}


if __name__ == "__main__":
    train_baseline()
