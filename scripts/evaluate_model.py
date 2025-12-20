import mlflow
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

DATA_DIR = Path("data/splits")


def evaluate_model(**context):
    test = pd.read_parquet(DATA_DIR / "test.parquet")

    target = "weekly_sales"
    features = [c for c in test.columns if c not in ["date", target]]

    # Get the latest run from the experiment
    experiment = mlflow.get_experiment_by_name("walmart_week3_baselines")
    if not experiment:
        raise RuntimeError("Experiment 'walmart_week3_baselines' not found")
    
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"], max_results=1)
    if runs.empty:
        raise RuntimeError("No runs found in experiment")
    
    latest_run_id = runs.iloc[0]["run_id"]
    model_uri = f"runs:/{latest_run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)

    X_test, y_test = test[features], test[target]
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    mlflow.log_metric("test_mae", mae)
    mlflow.log_metric("test_rmse", rmse)

    return {"test_mae": mae, "test_rmse": rmse}


if __name__ == "__main__":
    evaluate_model()
