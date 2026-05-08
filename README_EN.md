# SaaS Batch Data Pipeline

Versión en español de este README: [README.md](README.md)

> Controlled learning project focused on ELT fundamentals with BigQuery, dbt, Airflow and GitHub Actions using synthetic SaaS data.

## Description

End-to-end data engineering project to generate, load, transform, validate, and orchestrate synthetic SaaS data using Python, BigQuery, dbt, and Apache Airflow.

The pipeline builds a coherent synthetic source system with three tables (`users`, `subscriptions`, `events`), loads that data into BigQuery raw tables, applies layered transformations with dbt, runs basic data quality tests, and can be orchestrated with Airflow as an extension of the initial MVP.

The final result is a reproducible batch pipeline that can be executed end to end with a single local script and, in a second phase, also through an Airflow DAG.

## Project status

Functional version completed as a controlled learning environment:

- synthetic SaaS data generation
- raw loading into BigQuery
- staging and mart models with dbt
- basic data quality tests with dbt
- local end-to-end execution
- local Airflow orchestration
- lightweight validation with GitHub Actions

## Project goal

Build a reproducible batch pipeline focused on data engineering in order to practice:

- coherent synthetic data generation
- raw loading into BigQuery
- layered modeling with dbt
- basic data quality validation
- end-to-end execution with a single local runner
- basic pipeline orchestration with Airflow
- basic automated validation with GitHub Actions

## What this project demonstrates

- synthetic data generation in Python
- modeling of a simple SaaS source system with coherent entity relationships
- batch loading of CSV files into BigQuery
- design of `raw`, `staging`, and `marts` layers
- SQL transformations with dbt on top of BigQuery
- definition of basic data quality tests in dbt
- construction of reusable final models
- end-to-end execution through a reproducible runner
- local orchestration through Airflow with task-level separation
- use of XCom to pass small metadata between tasks
- basic automated validation through GitHub Actions
- clear separation between ingestion, transformation, validation, and orchestration

## Stack

- Python
- pandas
- BigQuery
- dbt
- Apache Airflow
- GitHub Actions
- SQL
- Git / GitHub
- VS Code
- WSL

## Repository structure

- `src/generate/`: synthetic data generation (`users`, `subscriptions`, `events`)
- `src/load/`: loading raw tables into BigQuery
- `src/utils/`: shared utilities such as logging
- `scripts/`: execution scripts and manual validation helpers
- `dbt_project/`: dbt project containing `staging` and `marts` models
- `airflow/dags/`: Airflow DAG definition for phase 2 orchestration
- `.github/workflows/`: CI workflow with GitHub Actions
- `data/generated/`: locally generated CSV files
- `docs/`: technical project documentation

## Pipeline flow

### Phase 1 — Local runner

1. generate `users`
2. generate `subscriptions` from `users`
3. generate `events` from `users` and `subscriptions`
4. save local CSV files
5. load raw tables into BigQuery in `saas_raw`
6. build `staging` models with dbt in `saas_staging`
7. build `marts` models with dbt in `saas_marts`
8. run basic data quality tests with dbt

### Phase 2 — Airflow orchestration

The same flow can also be executed through an Airflow DAG that separates the pipeline into explicit tasks for:

- synthetic table generation
- raw loading by table
- layered `dbt run` execution
- `dbt test` execution

## Data model

The synthetic source system is composed of three raw tables:

- `users`
- `subscriptions`
- `events`

Main relationships:

- one user can have many events
- in this first version of the project, one user can have zero or one subscription
- some events may be related to a subscription

BigQuery layers:

- `saas_raw`: generated and loaded data with minimal intervention
- `saas_staging`: cleaning, typing, and standardization with dbt
- `saas_marts`: final models for downstream consumption

## dbt models

### Staging

Cleaning and standardization models:

- `stg_users`
- `stg_subscriptions`
- `stg_events`

### Marts

Final models built on top of staging:

- `dim_users`
- `fct_subscriptions`
- `fct_events`
- `fct_user_activity`

## Data quality

The project includes basic dbt tests, including:

- `not_null`
- `unique`
- `relationships`

These tests are applied to primary keys and model relationships across staging and marts.

In addition, the repository includes a basic automated validation with GitHub Actions to verify core imports and run a lightweight synthetic generation smoke test on each `push` or `pull request`.

## Execution

### End-to-end execution with the local runner

    python -m scripts.run_pipeline

This command executes the full workflow:

- synthetic data generation
- local CSV persistence
- raw loading into BigQuery
- `dbt run`
- `dbt test`

### Orchestrated execution with Airflow

In phase 2, the pipeline can also be executed from Airflow through a local DAG, with task-level visibility, explicit dependencies, and logs available in the Airflow UI.

## Project phases

### Phase 1 — Reproducible batch MVP

The first phase of the project focused on building a local and reproducible batch pipeline with:

- synthetic data generation in Python
- raw loading into BigQuery
- layered transformations with dbt
- basic data quality tests
- end-to-end execution with a single local runner

### Phase 2 — Airflow orchestration

Once the MVP was validated, a second phase was added to explore orchestration:

- pipeline execution through an Airflow DAG
- flow separation into tasks
- explicit task dependencies
- XCom used to pass small metadata between tasks
- execution and observability through the Airflow UI

This second phase was implemented as an extension of the existing pipeline rather than a rewrite of the core logic.

## Technical documentation

Additional documentation available in:

- [Pipeline architecture](docs/architecture.md)
- [Data model](docs/data_model.md)

## Development note

This project was developed with support from AI tools as programming assistance to accelerate implementation, debugging, and documentation tasks.

The pipeline design, data model structure, simplification decisions, result validation, and final code review were carried out manually.

## Current limitations

- the pipeline remains batch and local
- the Airflow orchestration is implemented in a local learning environment, not in a production deployment
- the data is synthetic and does not represent a real production source
- the current data quality tests are basic
- the current CI only performs lightweight checks and does not execute the full pipeline with external services
- incremental loads are not implemented
- no dashboards or visualization layer are included

## Future improvements

- expand automated validation with additional structural or quality checks
- evolve the local orchestration setup toward a more production-like configuration
- add more advanced dbt tests
- evaluate incremental models
- incorporate seeds or macros where they provide real value
- add scheduling, retries, and alerts as the next orchestration step