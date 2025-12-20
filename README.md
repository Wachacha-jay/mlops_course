# MLOps Capstone 1 — Walmart Sales Pipeline

This project contains a small MLOps pipeline for ingesting and validating the Walmart weekly sales dataset.

Contents
- `scripts/download_data.py` — unzip/copy the Kaggle archive into `data/source/` and stage `data/raw/sales.csv`.
- `scripts/validate_data.py` — runs Great Expectations validation against `expectations/sales_expectation_suite.json`.
- `expectations/` — expectation suite used by Great Expectations.
- `data/` — local data (zip lives at top-level `data/walmart_archive.zip` for this workspace).

Quickstart
1. From the workspace root, change to the project folder:

```bash
cd mlops_capstone1_project
```

2. Ensure dependencies are installed in your Python environment (project uses `great_expectations`, `pandas`, etc.). Activate your venv if needed.

3. Place the dataset zip at the top-level `data/walmart_archive.zip` (already present in this workspace) and run the download script:

```bash
python3 scripts/download_data.py
```

This will extract CSV(s) to `data/source/` and copy the chosen CSV to `data/raw/sales.csv`.

4. Validate the raw CSV using Great Expectations:

```bash
python3 scripts/validate_data.py
```

If validation passes you will see a success log. If it fails, the script will raise and print the failing expectations.

Notes
- The expectation suite was adjusted to match the current CSV column names (`Store, Dept, Date, Weekly_Sales, IsHoliday`).
- `.gitignore` was added to ignore local venvs, data, and generated files.
- If you use DVC, ensure large data files are tracked with DVC and remotes configured.

Next steps
- Commit and push to a remote repository.
- Configure CI to run `scripts/validate_data.py` and/or the Airflow DAG.

Contact
- For questions about this workspace, check the `scripts/` and `expectations/` folders or ask the maintainer.

📜 Why Data Contracts Matter

In production machine learning systems, data is the most common point of failure. Unlike application code, data:

Changes silently

Comes from multiple upstream owners

Evolves without versioned APIs

Can degrade model performance without breaking pipelines

To address this, this project enforces data contracts at ingestion time using Great Expectations.

What Is a Data Contract?

A data contract is an explicit, executable agreement about:

Schema (columns, types, order)

Validity (ranges, allowed values)

Business logic (e.g., sales ≥ 0)

Tolerance to real-world noise (e.g., nullable markdowns)

These contracts are treated as first-class artifacts, versioned alongside code.

How This Project Enforces Data Contracts

During ingestion:

Raw data is staged into the pipeline

A Great Expectations suite validates:

Schema stability

Time format correctness

Non-negativity of sales and economic indicators

Controlled missingness in markdown features

The pipeline fails fast if expectations are violated

Only validated data is persisted and versioned

This prevents:

Silent schema drift

Corrupted training data

Undetected data quality regressions

Downstream model instability

Why This Matters for ML Systems

In real-world ML:

Most model “bugs” are actually data bugs

Retraining on bad data compounds errors

Monitoring only models is insufficient — data must be monitored first

By enforcing contracts at ingestion time, this project:

Shifts data quality checks left

Makes failures observable and debuggable

Creates reproducible, trustworthy datasets

Establishes a foundation for drift detection and governance in later stages

MLOps Principle Demonstrated

Models are disposable. Data integrity is not.

This Week 1 pipeline ensures that every downstream experiment, feature, and model is built on validated, versioned data with known guarantees.

