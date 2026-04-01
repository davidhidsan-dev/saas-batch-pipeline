# SaaS Batch Data Pipeline

English version of this README: [README_EN.md](README_EN.md)

## Descripción

Proyecto end-to-end de data engineering para generar, cargar, transformar, validar y orquestar datos sintéticos de un producto SaaS usando Python, BigQuery, dbt y Apache Airflow.

El pipeline construye una fuente sintética coherente con tres tablas (`users`, `subscriptions`, `events`), carga esos datos en BigQuery en la capa raw, aplica transformaciones por capas con dbt, ejecuta tests básicos de calidad y puede orquestarse mediante Airflow como extensión del MVP inicial.

El resultado final es un pipeline batch reproducible, ejecutable de extremo a extremo con un único script local y, en una segunda fase, también mediante un DAG de Airflow.

## Objetivo del proyecto

Construir un pipeline batch reproducible orientado a data engineering para practicar:

- generación de datos sintéticos coherentes
- carga raw en BigQuery
- modelado por capas con dbt
- validaciones básicas de calidad
- ejecución end-to-end con un único runner local
- orquestación básica del pipeline con Airflow
- validación automática básica con GitHub Actions

## Qué demuestra este proyecto

- generación de datos sintéticos en Python
- modelado de una fuente SaaS simple con relaciones coherentes entre entidades
- carga batch de archivos CSV a BigQuery
- diseño de capas `raw`, `staging` y `marts`
- transformaciones SQL con dbt sobre BigQuery
- definición de tests básicos de calidad en dbt
- construcción de modelos finales reutilizables
- ejecución end-to-end mediante un runner reproducible
- orquestación local mediante Airflow con separación por tasks
- uso de XCom para pasar metadatos pequeños entre tareas
- validación automática básica mediante GitHub Actions
- separación clara entre ingestión, transformación, validación y orquestación

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

## Estructura del repositorio

- `src/generate/`: generación de datos sintéticos (`users`, `subscriptions`, `events`)
- `src/load/`: carga de tablas raw a BigQuery
- `src/utils/`: utilidades compartidas como logging
- `scripts/`: scripts de ejecución y validación manual
- `dbt_project/`: proyecto dbt con modelos `staging` y `marts`
- `airflow/dags/`: definición del DAG de Airflow para la fase 2 de orquestación
- `.github/workflows/`: workflow de CI con GitHub Actions
- `data/generated/`: archivos CSV generados localmente
- `docs/`: documentación técnica del proyecto

## Flujo del pipeline

### Fase 1 — Runner local

1. generación de `users`
2. generación de `subscriptions` a partir de `users`
3. generación de `events` a partir de `users` y `subscriptions`
4. guardado local de archivos CSV
5. carga de tablas raw a BigQuery en `saas_raw`
6. construcción de modelos `staging` con dbt en `saas_staging`
7. construcción de modelos `marts` con dbt en `saas_marts`
8. ejecución de tests básicos de calidad con dbt

### Fase 2 — Orquestación con Airflow

El mismo flujo puede ejecutarse mediante un DAG de Airflow que separa el pipeline en tasks explícitas para:

- generación de tablas sintéticas
- carga raw por tabla
- ejecución de `dbt run` por capas
- ejecución de `dbt test`

## Modelo de datos

La fuente sintética se compone de tres tablas raw:

- `users`
- `subscriptions`
- `events`

Relaciones principales:

- un usuario puede tener muchos eventos
- en esta primera versión del proyecto, un usuario puede tener cero o una suscripción
- algunos eventos pueden estar relacionados con una suscripción

Capas en BigQuery:

- `saas_raw`: datos generados y cargados con mínima intervención
- `saas_staging`: limpieza, tipado y estandarización con dbt
- `saas_marts`: modelos finales para consumo posterior

## Modelos dbt

### Staging

Modelos de limpieza y estandarización:

- `stg_users`
- `stg_subscriptions`
- `stg_events`

### Marts

Modelos finales construidos sobre staging:

- `dim_users`
- `fct_subscriptions`
- `fct_events`
- `fct_user_activity`

## Calidad de datos

El proyecto incluye tests básicos en dbt, entre ellos:

- `not_null`
- `unique`
- `relationships`

Estos tests se aplican sobre claves principales y relaciones entre modelos staging y marts.

Además, el repositorio incluye una validación automática básica con GitHub Actions para comprobar imports principales y una prueba ligera de generación sintética en cada `push` o `pull request`.

## Ejecución

### Ejecución end-to-end con runner local

    python -m scripts.run_pipeline

Este comando ejecuta de extremo a extremo:

- generación de datos sintéticos
- persistencia local de CSV
- carga raw a BigQuery
- ejecución de `dbt run`
- ejecución de `dbt test`

### Ejecución orquestada con Airflow

En la fase 2, el pipeline puede ejecutarse también desde Airflow mediante un DAG local, con visibilidad por tasks, dependencias explícitas y logs desde la UI.

## Fases del proyecto

### Fase 1 — MVP batch reproducible

La primera fase del proyecto se centró en construir un pipeline batch local y reproducible con:

- generación de datos sintéticos en Python
- carga raw en BigQuery
- transformaciones por capas con dbt
- tests básicos de calidad
- ejecución end-to-end con un único script local

### Fase 2 — Orquestación con Airflow

Una vez validado el MVP, se añadió una segunda fase orientada a aprendizaje de orquestación:

- ejecución del pipeline mediante un DAG de Airflow
- separación del flujo en tasks
- definición explícita de dependencias
- uso de XCom para pasar metadatos pequeños entre tareas
- ejecución y observabilidad desde la UI de Airflow

Esta segunda fase se implementó como extensión del pipeline ya existente, sin rehacer la lógica principal del proyecto.

## Documentación técnica

Documentación adicional disponible en:

- [Arquitectura del pipeline](docs/architecture.md)
- [Modelo de datos](docs/data_model.md)

## Nota sobre el desarrollo

Este proyecto se desarrolló con apoyo de herramientas de IA como asistencia de programación para acelerar tareas de implementación, depuración y documentación.

El diseño del pipeline, la estructura del modelo de datos, las decisiones de simplificación, la validación de resultados y la revisión final del código fueron realizadas manualmente.

## Limitaciones actuales

- el pipeline sigue siendo batch y local
- la orquestación con Airflow está implementada en un entorno local de aprendizaje, no en un despliegue productivo
- los datos son sintéticos y no representan una fuente productiva real
- los tests actuales de calidad son básicos
- la CI actual valida solo comprobaciones ligeras y no ejecuta el pipeline completo con servicios externos
- no se implementan cargas incrementales
- no se incluyen dashboards ni capa de visualización

## Mejoras futuras

- ampliar la validación automática con pruebas adicionales de calidad o estructura
- evolucionar la orquestación local hacia una configuración más cercana a producción
- añadir tests más avanzados en dbt
- evaluar modelos incrementales
- incorporar seeds o macros donde aporten valor real
- añadir scheduling, retries y alertas como siguiente paso de orquestación