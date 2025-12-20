# MLOps Capstone 1: Walmart Sales Forecasting Pipeline

## Overview

This project implements a production-grade machine learning operations (MLOps) pipeline for Walmart weekly sales forecasting. It demonstrates end-to-end best practices including data ingestion, validation, feature engineering, model training, and experiment tracking.

**Key Features:**
- Data contract enforcement via Great Expectations
- Automated data validation and quality checks
- Feature engineering with lag and rolling statistics
- Baseline model training with scikit-learn
- MLflow experiment tracking and model registry
- Modular, DAG-based architecture (Airflow-ready)

## Project Structure

```
├── airflow/                          # Airflow DAGs for orchestration
│   └── dags/
│       ├── ingest_sales_dag.py       # Data ingestion and validation
│       ├── feature_pipeline_dag.py   # Feature engineering
│       └── training_pipeline_dag.py  # Model training and evaluation
├── scripts/                          # Core pipeline scripts
│   ├── download_data.py              # Data source setup
│   ├── validate_data.py              # Data contract validation (Great Expectations)
│   ├── feature_engineering.py        # Feature generation (lag, rolling stats)
│   ├── split_data.py                 # Train/test split
│   ├── train_baseline.py             # Model training with MLflow tracking
│   ├── evaluate_model.py             # Model evaluation on test set
│   ├── register_model.py             # Model registry operations
│   ├── log_data_metadata.py          # Data lineage tracking
│   ├── persist_data.py               # Data serialization
│   └── validate_feature.py           # Feature validation suite
├── expectations/                     # Great Expectations suites
│   ├── sales_expectation_suite.json  # Raw data contracts
│   └── feature_expectation_suite.json # Feature data contracts
├── data/                             # Data pipeline artifacts
│   ├── raw/                          # Raw ingested data
│   ├── source/                       # Source CSV files
│   ├── validated/                    # Validated data after QA
│   └── features/                     # Engineered features
├── mlruns/                           # MLflow tracking artifacts
└── pyproject.toml                    # Project dependencies and config
```

## Quickstart

### Prerequisites
- Python 3.11+
- Dependencies: `pandas`, `scikit-learn`, `great-expectations`, `mlflow`

### Setup

1. **Navigate to project directory:**
   ```bash
   cd mlops_capstone1_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or with conda
   conda env create -f environment.yml
   ```

3. **Prepare data source:**
   ```bash
   python3 scripts/download_data.py
   ```
   This extracts the Walmart sales dataset to `data/source/` and stages it as `data/raw/sales.csv`.

### Pipeline Execution

**Run the complete pipeline:**
```bash
# Data validation (enforces contracts)
python3 scripts/validate_data.py

# Feature engineering
python3 scripts/feature_engineering.py

# Train/test split
python3 scripts/split_data.py

# Model training with experiment tracking
python3 scripts/train_baseline.py

# Model evaluation
python3 scripts/evaluate_model.py
```

**Or use Airflow for orchestration:**
```bash
airflow dags list
airflow dags trigger ingest_sales_dag
airflow dags trigger feature_pipeline_dag
airflow dags trigger training_pipeline_dag
```

## Data Contracts

This project enforces explicit **data contracts** at ingestion and feature generation stages using Great Expectations.

### Raw Data Contract (`expectations/sales_expectation_suite.json`)

Validates:
- **Schema stability:** Expected columns (`Store`, `Dept`, `Date`, `Weekly_Sales`, `IsHoliday`)
- **Data types:** Proper type enforcement (numeric, datetime)
- **Business constraints:** Non-negative sales values
- **Completeness:** Acceptable missingness thresholds

### Feature Contract (`expectations/feature_expectation_suite.json`)

Validates:
- **Feature stability:** All engineered features present
- **Statistical bounds:** Lag and rolling features within expected ranges
- **No data leakage:** Forward-looking features properly lagged

### Why Data Contracts Matter

In production ML systems, data is the primary source of failures:
- **Silent drift:** Schema changes without detection
- **Corrupted training:** Bad upstream data → bad models
- **Unmonitored degradation:** Model performance drops due to data quality, not model issues

By enforcing contracts at ingestion, this pipeline:
- ✅ Fails fast on invalid data
- ✅ Prevents downstream model contamination
- ✅ Creates reproducible, auditable datasets
- ✅ Enables early drift detection

**Core MLOps Principle:** *Models are disposable. Data integrity is not.*

## Model Tracking

All experiments are tracked in MLflow under the `walmart_week3_baselines` experiment:

```bash
# View experiments
mlflow ui --backend-store-uri file:./mlruns

# Query specific run
mlflow runs list --experiment-name walmart_week3_baselines
```

**Tracked artifacts:**
- Model serialization (sklearn pickle)
- Hyperparameters
- Train/test metrics (MAE, RMSE)
- Feature importance and validation results

## Configuration

Key paths and settings can be configured in individual scripts:

| Script | Key Variables |
|--------|---------------|
| `validate_data.py` | `RAW_DATA_PATH`, `EXPECTATION_SUITE_NAME` |
| `feature_engineering.py` | `INPUT_PATH`, `OUTPUT_PATH` |
| `train_baseline.py` | Model type, hyperparameters, experiment name |

## Development & Contributing

- **Code style:** Follow PEP 8 conventions
- **Testing:** Add unit tests for pipeline scripts in `tests/`
- **Documentation:** Update `expectations/` JSONs when schema changes
- **DVC (optional):** Track large data files with `dvc add` and push to remote storage

## Troubleshooting

| Error | Solution |
|-------|----------|
| `FileNotFoundError: Validated data not found` | Run `validate_data.py` first |
| `Run 'latest' not found` | Ensure `train_baseline.py` has been executed |
| `Missing column 'date'` | Check CSV column names match expectations |

## Next Steps

- [ ] Deploy pipeline to production orchestrator (Airflow, Prefect, Dagster)
- [ ] Add data drift monitoring with Great Expectations
- [ ] Implement model performance monitoring
- [ ] Set up automated retraining triggers
- [ ] Configure DVC remotes for data versioning
- [ ] Add integration tests and CI/CD

## References

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [MLflow Guide](https://mlflow.org/docs/latest/index.html)
- [Walmart Sales Dataset](https://www.kaggle.com/datasets/walmart/walmart-recruiting-store-sales-forecasting)

## License

This project is part of the MLOps Capstone course.
