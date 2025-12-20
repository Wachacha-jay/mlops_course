import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest
from pathlib import Path

FEATURES_PATH = Path("data/features/sales_features.parquet")
SUITE_NAME = "feature_expectation_suite"


def validate_features(**context):
    context_ge = ge.get_context()

    batch_request = RuntimeBatchRequest(
        datasource_name="walmart_sales_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="sales_features",
        runtime_parameters={"path": str(FEATURES_PATH)},
        batch_identifiers={"default_identifier_name": "features"},
    )

    suite = context_ge.get_expectation_suite(SUITE_NAME)
    validator = context_ge.get_validator(batch_request, suite)

    results = validator.validate()

    if not results.success:
        raise ValueError("Feature validation failed")

    return True


if __name__ == "__main__":
    validate_features()
