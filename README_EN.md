# SaaS Batch Data Pipeline

Versión en español de este README: [README.md](README.md)

## Description

End-to-end data engineering project to generate, load, transform, and validate synthetic SaaS data using Python, BigQuery, and dbt.

The pipeline builds a coherent synthetic source system with three tables (`users`, `subscriptions`, `events`), loads that data into BigQuery raw tables, applies layered transformations with dbt, and runs basic data quality tests.

The final result is a reproducible batch pipeline that can be executed end to end with a single local script.

## Project goal

Build a reproducible batch pipeline focused on data engineering in order to practice:

- coherent synthetic data generation
- raw loading into BigQuery
- layered modeling with dbt
- basic data quality validation
- end-to-end execution with a single local runner

## What this project demonstrates

- synthetic data generation in Python
- modeling of a simple SaaS source system with coherent entity relationships
- batch loading of CSV files into BigQuery
- design of `raw`, `staging`, and `marts` layers
- SQL transformations with dbt on top of BigQuery
- definition of basic data quality tests in dbt
- construction of reusable final models
- end-to-end execution through a reproducible runner
- clear separation between ingestion, transformation, and validation

## Stack

- Python
- pandas
- BigQuery
- dbt
- SQL
- Git / GitHub
- VS Code

## Repository structure

- `src/generate/`: synthetic data generation (`users`, `subscriptions`, `events`)
- `src/load/`: loading raw tables into BigQuery
- `src/utils/`: shared utilities such as logging
- `scripts/`: execution scripts and manual validation helpers
- `dbt_project/`: dbt project containing `staging` and `marts` models
- `data/generated/`: locally generated CSV files
- `docs/`: technical project documentation

## Pipeline flow

1. generate `users`
2. generate `subscriptions` from `users`
3. generate `events` from `users` and `subscriptions`
4. save local CSV files
5. load raw tables into BigQuery in `saas_raw`
6. build `staging` models with dbt in `saas_staging`
7. build `marts` models with dbt in `saas_marts`
8. run basic data quality tests with dbt

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

## Execution

Example of end-to-end pipeline execution:

    python -m scripts.run_pipeline

This command executes the full workflow:

- synthetic data generation
- local CSV persistence
- raw loading into BigQuery
- `dbt run`
- `dbt test`

## Technical documentation

Additional documentation available in:

- [Pipeline architecture](docs/architecture.md)
- [Data model](docs/data_model.md)

## Development note

This project was developed with support from AI tools as programming assistance to accelerate implementation, debugging, and documentation tasks.

The pipeline design, data model structure, simplification decisions, result validation, and final code review were carried out manually.

## Current limitations

- the pipeline is batch and local, not orchestrated
- the data is synthetic and does not represent a real production source
- the current data quality tests are basic
- incremental loads are not implemented
- orchestration is not included in this first phase
- no dashboards or visualization layer are included

## Future improvements

- introduce orchestration with Apache Airflow or a lighter alternative
- add more advanced dbt tests
- evaluate incremental models
- incorporate seeds or macros where they provide real value
- add more automation for deployment or validation