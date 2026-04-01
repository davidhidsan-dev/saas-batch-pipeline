# Pipeline Architecture / Arquitectura del Pipeline

## ES — Objetivo de la arquitectura

Este proyecto implementa un pipeline batch local orientado a data engineering.

El objetivo es simular un flujo end-to-end sencillo y reproducible en el que:

- Python genera datos sintéticos coherentes
- Python carga esos datos en BigQuery en la capa raw
- dbt transforma los datos en capas staging y marts
- dbt ejecuta tests básicos de calidad
- un script local permite ejecutar el pipeline completo de extremo a extremo
- una capa adicional de orquestación con Airflow permite ejecutar el mismo flujo mediante tasks explícitas

La arquitectura está diseñada para priorizar comprensión, reproducibilidad y separación clara de responsabilidades.

## ES — Componentes principales

La arquitectura se compone de cinco bloques principales:

### 1. Generación de datos
La generación de datos se implementa en Python.

En este proyecto:

- Python actúa como simulador de una fuente operativa SaaS
- genera tres tablas sintéticas: `users`, `subscriptions` y `events`
- los datos siguen reglas mínimas de coherencia entre entidades

La responsabilidad de esta capa es producir datos fuente consistentes para el resto del pipeline.

### 2. Carga a BigQuery
La carga a BigQuery también se implementa en Python.

En este proyecto:

- los datos generados se guardan localmente como archivos intermedios
- posteriormente se cargan en BigQuery en el dataset `saas_raw`
- esta carga representa la capa raw o de ingestión

La responsabilidad de esta capa es mover los datos desde la generación local hasta la plataforma analítica sin aplicar transformaciones de negocio complejas.

### 3. Transformación con dbt
La transformación principal se implementa con dbt sobre BigQuery.

En este proyecto:

- la capa `saas_staging` limpia, tipa y estandariza los datos raw
- la capa `saas_marts` construye modelos finales simples y explicables
- la lógica principal de transformación vive en SQL y dbt, no en Python

La responsabilidad de esta capa es convertir datos raw en modelos estructurados y reutilizables.

### 4. Validación de calidad
La validación de calidad se implementa con tests de dbt.

En este proyecto:

- se aplican tests básicos sobre claves, nulos y relaciones
- los tests se ejecutan después de construir los modelos
- el objetivo es validar consistencia mínima del pipeline

La responsabilidad de esta capa es detectar errores estructurales y reforzar la confianza en los modelos construidos.

### 5. Orquestación y automatización
La orquestación se implementa en una segunda fase mediante Apache Airflow.

En este proyecto:

- Airflow no reemplaza la lógica del pipeline
- Airflow divide el flujo en tasks explícitas
- Airflow modela dependencias entre generación, carga raw, transformaciones y tests
- Airflow permite observar la ejecución desde su UI
- GitHub Actions añade una validación automática ligera sobre el repositorio

La responsabilidad de esta capa es coordinar la ejecución del pipeline y añadir una primera base de automatización y observabilidad.

## ES — Datasets y capas

La arquitectura utiliza tres datasets en BigQuery:

- `saas_raw`
- `saas_staging`
- `saas_marts`

Estas capas representan distintas etapas del pipeline:

### `saas_raw`
Contiene datos generados y cargados con mínima intervención.

Esta capa conserva la estructura de la fuente sintética y actúa como punto de entrada al warehouse.

### `saas_staging`
Contiene modelos dbt de limpieza e integración básica.

Esta capa prepara los datos para consumo posterior mediante tipado, renombrado y estandarización.

### `saas_marts`
Contiene modelos dbt finales.

Esta capa expone tablas limpias y comprensibles para uso analítico o para futuras ampliaciones del proyecto.

## ES — Flujo de ejecución

La arquitectura actual admite dos formas principales de ejecución.

### Fase 1 — Runner local
El pipeline sigue este orden:

1. generar `users`
2. generar `subscriptions`
3. generar `events`
4. guardar archivos generados localmente
5. cargar tablas en `saas_raw`
6. ejecutar modelos dbt de staging
7. ejecutar modelos dbt de marts
8. ejecutar tests dbt

Este flujo refleja las dependencias entre entidades y separa claramente ingestión, transformación y validación.

### Fase 2 — Orquestación con Airflow
En la segunda fase, el mismo pipeline se ejecuta mediante un DAG de Airflow que separa el flujo en tasks como:

- generación de `users`
- generación de `subscriptions`
- generación de `events`
- carga raw de `users`
- carga raw de `subscriptions`
- carga raw de `events`
- ejecución de `dbt run` para staging
- ejecución de `dbt run` para marts
- ejecución de `dbt test`

Esto añade visibilidad por tarea, dependencias explícitas y observabilidad desde la UI de Airflow.

## ES — Responsabilidad de cada tecnología

En este proyecto, cada tecnología tiene una función concreta:

### Python
Se utiliza para:

- generación de datos sintéticos
- persistencia local de archivos intermedios
- carga a BigQuery
- ejecución secuencial del pipeline completo en la fase 1

### BigQuery
Se utiliza para:

- almacenamiento de datos raw
- ejecución de modelos dbt
- almacenamiento de capas staging y marts

### dbt
Se utiliza para:

- modelado SQL por capas
- estandarización y transformación de datos
- definición y ejecución de tests de calidad

### Airflow
Se utiliza para:

- definir el DAG del pipeline
- separar el flujo en tasks
- expresar dependencias entre tareas
- ejecutar el pipeline con visibilidad operativa desde la UI

### GitHub Actions
Se utiliza para:

- ejecutar una validación automática ligera del repositorio
- comprobar imports principales
- ejecutar una smoke test básica de generación sintética en cada `push` o `pull request`

Esta separación busca que cada herramienta se use para aquello que mejor resuelve.

## ES — Decisiones de simplificación

La arquitectura adopta varias decisiones deliberadas para mantener el proyecto manejable y comprensible.

En este proyecto:

- el MVP inicial se construyó sin orquestador
- Airflow se añadió solo después de validar el pipeline base
- no se incluyen dashboards
- no se implementa streaming
- no se despliega infraestructura productiva adicional
- la CI actual es ligera y no ejecuta el pipeline completo con servicios externos

Esto significa que el foco del proyecto está en:

- diseño del pipeline batch
- modelado de datos por capas
- transformación con SQL y dbt
- comprensión completa del flujo
- introducción progresiva a orquestación y automatización

## ES — Estado actual de la arquitectura

Actualmente el proyecto cuenta con dos niveles principales de implementación:

### Fase 1
Pipeline batch reproducible con Python, BigQuery y dbt.

### Fase 2
Orquestación local con Airflow y validación automática ligera con GitHub Actions.

La fase 2 no sustituye la lógica principal del pipeline, sino que añade una capa de coordinación, visibilidad y automatización básica sobre un pipeline ya funcional.

---

## EN — Architecture objective

This project implements a local batch pipeline focused on data engineering.

The goal is to simulate a simple and reproducible end-to-end flow where:

- Python generates coherent synthetic data
- Python loads that data into BigQuery raw tables
- dbt transforms the data into staging and marts layers
- dbt runs basic data quality tests
- a local script can execute the full pipeline end to end
- an additional orchestration layer with Airflow can execute the same flow through explicit tasks

The architecture is designed to prioritize understanding, reproducibility, and clear separation of responsibilities.

## EN — Main components

The architecture is composed of five main blocks:

### 1. Data generation
Data generation is implemented in Python.

In this project:

- Python acts as a simulator of a SaaS operational source
- it generates three synthetic tables: `users`, `subscriptions`, and `events`
- the data follows minimum consistency rules across entities

The responsibility of this layer is to produce source data that is coherent enough for the rest of the pipeline.

### 2. BigQuery load
Loading into BigQuery is also implemented in Python.

In this project:

- generated data is stored locally as intermediate files
- it is then loaded into BigQuery in the `saas_raw` dataset
- this load represents the raw ingestion layer

The responsibility of this layer is to move data from local generation into the analytical platform without applying complex business transformations.

### 3. Transformation with dbt
The main transformation logic is implemented with dbt on top of BigQuery.

In this project:

- the `saas_staging` layer cleans, casts, and standardizes raw data
- the `saas_marts` layer builds final models that are simple and explainable
- the main transformation logic lives in SQL and dbt, not in Python

The responsibility of this layer is to convert raw data into structured and reusable models.

### 4. Data quality validation
Data quality validation is implemented through dbt tests.

In this project:

- basic tests are applied on keys, nulls, and relationships
- tests run after models are built
- the goal is to validate the minimum consistency of the pipeline

The responsibility of this layer is to detect structural issues and reinforce trust in the built models.

### 5. Orchestration and automation
Orchestration is implemented in a second phase with Apache Airflow.

In this project:

- Airflow does not replace pipeline logic
- Airflow breaks the flow into explicit tasks
- Airflow models dependencies between generation, raw loading, transformations, and tests
- Airflow makes execution observable through its UI
- GitHub Actions adds lightweight automated validation for the repository

The responsibility of this layer is to coordinate pipeline execution and add an initial foundation of automation and observability.

## EN — Datasets and layers

The architecture uses three BigQuery datasets:

- `saas_raw`
- `saas_staging`
- `saas_marts`

These layers represent different stages of the pipeline:

### `saas_raw`
Contains generated and loaded data with minimal intervention.

This layer preserves the structure of the synthetic source and acts as the entry point into the warehouse.

### `saas_staging`
Contains dbt models for cleaning and basic integration.

This layer prepares data for downstream use through casting, renaming, and standardization.

### `saas_marts`
Contains final dbt models.

This layer exposes clean and understandable tables for analytical use or future project extensions.

## EN — Execution flow

The current architecture supports two main execution modes.

### Phase 1 — Local runner
The pipeline follows this order:

1. generate `users`
2. generate `subscriptions`
3. generate `events`
4. save generated files locally
5. load tables into `saas_raw`
6. run dbt staging models
7. run dbt marts models
8. run dbt tests

This flow reflects entity dependencies and clearly separates ingestion, transformation, and validation.

### Phase 2 — Airflow orchestration
In the second phase, the same pipeline is executed through an Airflow DAG that separates the flow into tasks such as:

- `users` generation
- `subscriptions` generation
- `events` generation
- raw loading of `users`
- raw loading of `subscriptions`
- raw loading of `events`
- `dbt run` for staging
- `dbt run` for marts
- `dbt test`

This adds task-level visibility, explicit dependencies, and observability through the Airflow UI.

## EN — Responsibility of each technology

In this project, each technology has a specific role:

### Python
Used for:

- synthetic data generation
- local persistence of intermediate files
- BigQuery loading
- sequential execution of the full pipeline in phase 1

### BigQuery
Used for:

- raw data storage
- execution of dbt models
- storage of staging and marts layers

### dbt
Used for:

- layered SQL modeling
- data standardization and transformation
- definition and execution of data quality tests

### Airflow
Used for:

- defining the pipeline DAG
- separating the flow into tasks
- expressing task dependencies
- executing the pipeline with operational visibility through the UI

### GitHub Actions
Used for:

- running lightweight automated repository validation
- checking core imports
- running a basic synthetic generation smoke test on each `push` or `pull request`

This separation is intended to use each tool for what it solves best.

## EN — Simplification decisions

The architecture adopts several deliberate simplification decisions to keep the project manageable and understandable.

In this project:

- the initial MVP was built without an orchestrator
- Airflow was added only after the base pipeline was validated
- no dashboards are included
- no streaming is implemented
- no production infrastructure is deployed
- the current CI is lightweight and does not run the full pipeline against external services

This means the project focuses on:

- batch pipeline design
- layered data modeling
- transformation with SQL and dbt
- full understanding of the flow
- gradual introduction to orchestration and automation

## EN — Current architecture state

The project currently has two main implementation levels:

### Phase 1
A reproducible batch pipeline with Python, BigQuery, and dbt.

### Phase 2
Local orchestration with Airflow and lightweight automated validation with GitHub Actions.

Phase 2 does not replace the core pipeline logic. Instead, it adds a layer of coordination, visibility, and basic automation on top of an already functional pipeline.