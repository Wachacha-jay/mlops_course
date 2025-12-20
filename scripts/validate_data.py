# scripts/validate_data.py

from pathlib import Path
import logging
import json
import shutil
import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.datasource.fluent import (
    PandasFilesystemDatasource,
    batch_request as fluent_batch_request,
)

RAW_DATA_PATH = Path("data/raw/sales.csv")
EXPECTATION_SUITE_NAME = "sales_expectation_suite"
EXPECTATIONS_DIR = Path("expectations")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_data(**context):
    """
    Validates raw Walmart sales data using Great Expectations.

    Fails fast if validation does not pass.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw data not found at {RAW_DATA_PATH}")

    # Initialize GE context
    context_ge = ge.get_context()

    # Register a fluent Pandas filesystem datasource (base dir -> data/source)
    datasource_name = "walmart_sales_datasource"

    if datasource_name not in [ds["name"] for ds in context_ge.list_datasources()]:
        ds = PandasFilesystemDatasource(name=datasource_name, base_directory=Path("data/source"))
        context_ge.add_datasource(datasource=ds)
        # register a CSV asset name that we'll reference in the BatchRequest
        ds.add_csv_asset("walmart_sales")

    # Build a fluent BatchRequest for the specific CSV file name
    data_asset_name = "walmart_sales"
    # Determine the filename under the datasource base_directory
    source_dir = Path("data/source")
    candidate = Path(RAW_DATA_PATH).name
    if (source_dir / candidate).exists():
        filename = candidate
    elif (source_dir / "train.csv").exists():
        filename = "train.csv"
    elif (source_dir / "sales.csv").exists():
        filename = "sales.csv"
    else:
        raise FileNotFoundError(f"No source CSV found in {source_dir}")
    batch_request = fluent_batch_request.BatchRequest(
        datasource_name=datasource_name,
        data_asset_name=data_asset_name,
        options={"path": filename},
    )

    # Load expectation suite from local JSON (convert legacy keys)
    expectations_path = Path("expectations") / f"{EXPECTATION_SUITE_NAME}.json"
    if not expectations_path.exists():
        raise RuntimeError(f"Expectation suite file not found at {expectations_path}")

    with open(expectations_path) as fh:
        suite_json = json.load(fh)

    # Older exports used 'expectation_type' keys; convert to 'type'/'kwargs'
    converted = []
    for e in suite_json.get("expectations", []):
        converted.append({"type": e.get("expectation_type"), "kwargs": e.get("kwargs", {})})

    suite = ExpectationSuite(name=suite_json.get("expectation_suite_name", EXPECTATION_SUITE_NAME), expectations=converted, meta=suite_json.get("meta", {}))

    # Validator
    validator = context_ge.get_validator(
        batch_request=batch_request,
        expectation_suite=suite,
    )

    results = validator.validate()

    if not results.success:
        logger.error("Data validation failed")
        raise ValueError("Great Expectations validation failed")

    logger.info("Data validation passed successfully")

    # Save validated data (copy the same source CSV we validated)
    validated_output_path = Path("data/validated/sales_validated.csv")
    validated_output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_dir / filename, validated_output_path)
    logger.info("Validated data written to %s", validated_output_path)

    return {
        "validated_rows": results.statistics["evaluated_expectations"],
        "success": True,
        "output_path": str(validated_output_path),
    }


if __name__ == "__main__":
    validate_data()
