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

## Code Quality

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

## Notes

ETL SQL is generated automatically and saved under _data/generated_outputs/sql/etl.sql_.

Views such as _user_metrics_view__staging_ and _user_metrics_view_ are created dynamically.

You can add new metrics editing `aggregates` in the [sql generation prompt](genaidrivenetl/prompts/transformation_generation.txt).
As well, you can generate new tests by editing `required_checks` in the [test generation prompt](genaidrivenetl/prompts/test_generation.txt).
The project uses Poetry for reproducible environments. Check [config file](genaidrivenetl/config.py).

---

## Screenshots

1. Prompt to generate SQL query
![img_1.png](screenshots/img_1.png)
2. Generated SQL
![img_2.png](screenshots/img_2.png)
3. Prompt for test generation
![img_3.png](screenshots/img_3.png)
4. Generated tests  
![img_4.png](screenshots/img_4.png)
5. Run generated tests
![img_5.png](screenshots/img_5.png)  
Executed generated SQL queries on user event streams and transactional data to produce analytics metrics and validate results  
6. Update the table if tests completed successfully (stage —> prod)
![img_6.png](screenshots/img_6.png)
