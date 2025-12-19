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
