# Pipeline Architecture / Arquitectura del Pipeline

## ES — Objetivo de la arquitectura

Este proyecto implementa un pipeline batch local orientado a data engineering.

El objetivo es simular un flujo end-to-end sencillo y reproducible en el que:

- Python genera datos sintéticos coherentes
- Python carga esos datos en BigQuery en la capa raw
- dbt transforma los datos en capas staging y marts
- dbt ejecuta tests básicos de calidad
- un único script local ejecuta el pipeline completo

La arquitectura está diseñada para priorizar comprensión, reproducibilidad y separación clara de responsabilidades.

## ES — Componentes principales

La arquitectura se compone de cuatro bloques principales:

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
- la lógica principal de transformación debe vivir en SQL y dbt, no en Python

La responsabilidad de esta capa es convertir datos raw en modelos estructurados y reutilizables.

### 4. Validación de calidad
La validación de calidad se implementa con tests de dbt.

En este proyecto:

- se aplican tests básicos sobre claves, nulos y relaciones
- los tests se ejecutan después de construir los modelos
- el objetivo es validar consistencia mínima del pipeline

La responsabilidad de esta capa es detectar errores estructurales y reforzar la confianza en los modelos construidos.

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

El pipeline sigue este orden:

1. generar `users`
2. generar `subscriptions`
3. generar `events`
4. guardar archivos generados localmente
5. cargar tablas en `saas_raw`
6. ejecutar modelos dbt de staging
7. ejecutar modelos dbt de marts
8. ejecutar tests dbt

Este orden refleja las dependencias entre entidades y separa claramente ingestión, transformación y validación.

## ES — Responsabilidad de cada tecnología

En este proyecto, cada tecnología tiene una función concreta:

### Python
Se utiliza para:

- generación de datos sintéticos
- persistencia local de archivos intermedios
- carga a BigQuery
- ejecución secuencial del pipeline completo

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

Esta separación busca que cada herramienta se use para aquello que mejor resuelve.

## ES — Decisiones de simplificación

La arquitectura adopta varias decisiones deliberadas para mantener el proyecto manejable en una primera fase.

En este proyecto:

- no se utiliza orquestador al inicio
- no se incluyen dashboards
- no se implementa streaming
- no se añade CI/CD en la fase inicial
- no se despliega infraestructura adicional innecesaria

Esto significa que el foco del MVP está en:

- diseño del pipeline batch
- modelado de datos por capas
- transformación con SQL y dbt
- comprensión completa del flujo

## ES — Evolución prevista en fase 2

Una vez validado el pipeline batch local, el proyecto podrá ampliarse con una capa de orquestación.

En esa fase:

- se evaluará introducir Apache Airflow o una alternativa más simple
- el objetivo será orquestar tareas ya existentes, no rehacer el pipeline
- la orquestación deberá aportar visibilidad, orden y automatización reales

Esto implica que la fase 2 se construirá sobre un pipeline ya entendido y funcional.

---

## EN — Architecture objective

This project implements a local batch pipeline focused on data engineering.

The goal is to simulate a simple and reproducible end-to-end flow where:

- Python generates coherent synthetic data
- Python loads that data into BigQuery raw tables
- dbt transforms the data into staging and marts layers
- dbt runs basic data quality tests
- a single local script executes the full pipeline

The architecture is designed to prioritize understanding, reproducibility and clear separation of responsibilities.

## EN — Main components

The architecture is composed of four main blocks:

### 1. Data generation
Data generation is implemented in Python.

In this project:

- Python acts as a simulator of a SaaS operational source
- it generates three synthetic tables: `users`, `subscriptions` and `events`
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

- the `saas_staging` layer cleans, casts and standardizes raw data
- the `saas_marts` layer builds final models that are simple and explainable
- the main transformation logic should live in SQL and dbt, not in Python

The responsibility of this layer is to convert raw data into structured and reusable models.

### 4. Data quality validation
Data quality validation is implemented through dbt tests.

In this project:

- basic tests are applied on keys, nulls and relationships
- tests run after models are built
- the goal is to validate the minimum consistency of the pipeline

The responsibility of this layer is to detect structural issues and reinforce trust in the built models.

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

This layer prepares data for downstream use through casting, renaming and standardization.

### `saas_marts`
Contains final dbt models.

This layer exposes clean and understandable tables for analytical use or future project extensions.

## EN — Execution flow

The pipeline follows this order:

1. generate `users`
2. generate `subscriptions`
3. generate `events`
4. save generated files locally
5. load tables into `saas_raw`
6. run dbt staging models
7. run dbt marts models
8. run dbt tests

This order reflects entity dependencies and clearly separates ingestion, transformation and validation.

## EN — Responsibility of each technology

In this project, each technology has a specific role:

### Python
Used for:

- synthetic data generation
- local persistence of intermediate files
- BigQuery loading
- sequential execution of the full pipeline

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

This separation is intended to use each tool for what it solves best.

## EN — Simplification decisions

The architecture adopts several deliberate simplification decisions to keep the project manageable in its first phase.

In this project:

- no orchestrator is used initially
- no dashboards are included
- no streaming is implemented
- no CI/CD is added in the initial phase
- no unnecessary infrastructure is introduced

This means that the MVP focuses on:

- batch pipeline design
- layered data modeling
- transformation with SQL and dbt
- full understanding of the flow

## EN — Expected phase 2 evolution

Once the local batch pipeline is validated, the project may be extended with an orchestration layer.

In that phase:

- Apache Airflow or a simpler alternative will be evaluated
- the goal will be to orchestrate existing tasks, not rebuild the pipeline
- orchestration should add real visibility, structure and automation

This means phase 2 will be built on top of a pipeline that is already understood and working.