# GenAI-Driven ETL Workflow Generator

**GenAIDrivenETL** is an ETL pipeline project powered by generative AI. It generates SQL transformations and corresponding tests for session metrics and other analytics derived from raw event data.

---

## Features

- Generates production-ready SQL transformations from raw schema and business rules.
- Supports PostgreSQL local database.
- Automatically creates views for session metrics.
- Generates `pytest` tests to validate data quality.
- Includes Poetry for dependency management.
- Built-in PEP8 linting and formatting with Black, isort, and Flake8.

---

## GenAI Usage

- Schema modeling from business rules
- SQL transformation generation
- Test automation

---

## Stack

Python, PostgreSQL, LLM API, pytest

---

## Run

1. Start Postgres
2. Load sample data
3. Run pipeline:

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/romandevyatov/GenAIDrivenETL.git
cd GenAIDrivenETL
```

2. Create .env file in the project root:

 * OPENROUTER_API_KEY=your_openrouter_key
 * DB_NAME=genai_etl_db_any
 * DB_HOST=localhost
 * DB_PORT=5432
 * DB_USER=your_db_user
 * DB_PASSWORD=your_db_password
 * VIEW_NAME=your_table_name_any
 * STAGING_VIEW_NAME=your_staging_table_name_any

3. Run pipeline:
```bash
./scripts/run_all.sh
```
- _This script sequentially runs:_
  - init_db.sh
  - run_main_pipeline.sh
  - run_generated_tests.sh
  - run_commit_views.sh
  - run_lint.sh

P.S.: (On-MacOS) Make shell scripts executable:
```bash
chmod +x ./scripts/*.sh
```

---

Code Quality

Autoformat code with Black and isort:

```bash
poetry run black genaidrivenetl tests
poetry run isort genaidrivenetl tests
```

Check PEP8 compliance with Flake8:
```bash
poetry run flake8 genaidrivenetl tests
```

Optional: Run full lint script:
```bash
./scripts/run_lint.sh
```
---

Notes

ETL SQL is generated automatically and saved under data/generated_outputs/sql/etl.sql.

Views such as user_metrics_view__staging and user_metrics_view are created dynamically.

The project uses Poetry for reproducible environments.
