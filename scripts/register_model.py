import mlflow


def register_model(**context):
    client = mlflow.tracking.MlflowClient()
    run_id = client.search_runs(
        experiment_ids=["0"], order_by=["metrics.val_rmse ASC"]
    )[0].info.run_id

    mlflow.register_model(
        model_uri=f"runs:/{run_id}/model",
        name="WalmartSalesForecast"
    )


if __name__ == "__main__":
    register_model()
