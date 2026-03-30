# SaaS Batch Data Pipeline

English version of this README: [README_EN.md](README_EN.md)

## Descripción

Proyecto end-to-end de data engineering para generar, cargar, transformar y validar datos sintéticos de un producto SaaS usando Python, BigQuery y dbt.

El pipeline construye una fuente sintética coherente con tres tablas (`users`, `subscriptions`, `events`), carga esos datos en BigQuery en la capa raw, aplica transformaciones por capas con dbt y ejecuta tests básicos de calidad.

El resultado final es un pipeline batch reproducible, ejecutable de extremo a extremo con un único script local.

## Objetivo del proyecto

Construir un pipeline batch reproducible orientado a data engineering para practicar:

- generación de datos sintéticos coherentes
- carga raw en BigQuery
- modelado por capas con dbt
- validaciones básicas de calidad
- ejecución end-to-end con un único runner local

## Qué demuestra este proyecto

- generación de datos sintéticos en Python
- modelado de una fuente SaaS simple con relaciones coherentes entre entidades
- carga batch de archivos CSV a BigQuery
- diseño de capas `raw`, `staging` y `marts`
- transformaciones SQL con dbt sobre BigQuery
- definición de tests básicos de calidad en dbt
- construcción de modelos finales reutilizables
- ejecución end-to-end mediante un runner reproducible
- separación clara entre ingestión, transformación y validación

## Stack

- Python
- pandas
- BigQuery
- dbt
- SQL
- Git / GitHub
- VS Code

## Estructura del repositorio

- `src/generate/`: generación de datos sintéticos (`users`, `subscriptions`, `events`)
- `src/load/`: carga de tablas raw a BigQuery
- `src/utils/`: utilidades compartidas como logging
- `scripts/`: scripts de ejecución y validación manual
- `dbt_project/`: proyecto dbt con modelos `staging` y `marts`
- `data/generated/`: archivos CSV generados localmente
- `docs/`: documentación técnica del proyecto

## Flujo del pipeline

1. generación de `users`
2. generación de `subscriptions` a partir de `users`
3. generación de `events` a partir de `users` y `subscriptions`
4. guardado local de archivos CSV
5. carga de tablas raw a BigQuery en `saas_raw`
6. construcción de modelos `staging` con dbt en `saas_staging`
7. construcción de modelos `marts` con dbt en `saas_marts`
8. ejecución de tests básicos de calidad con dbt

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

## Ejecución

Ejemplo de ejecución end-to-end del pipeline:

    python -m scripts.run_pipeline

Este comando ejecuta de extremo a extremo:

- generación de datos sintéticos
- persistencia local de CSV
- carga raw a BigQuery
- ejecución de `dbt run`
- ejecución de `dbt test`

## Documentación técnica

Documentación adicional disponible en:

- [Arquitectura del pipeline](docs/architecture.md)
- [Modelo de datos](docs/data_model.md)

## Nota sobre el desarrollo

Este proyecto se desarrolló con apoyo de herramientas de IA como asistencia de programación para acelerar tareas de implementación, depuración y documentación.

El diseño del pipeline, la estructura del modelo de datos, las decisiones de simplificación, la validación de resultados y la revisión final del código fueron realizadas manualmente.

## Limitaciones actuales

- el pipeline es batch y local, no orquestado
- los datos son sintéticos y no representan una fuente productiva real
- los tests actuales de calidad son básicos
- no se implementan cargas incrementales
- no se incluye orquestación en esta primera fase
- no se incluyen dashboards ni capa de visualización

## Mejoras futuras

- introducir orquestación con Apache Airflow o una alternativa más ligera
- añadir tests más avanzados en dbt
- evaluar modelos incrementales
- incorporar seeds o macros donde aporten valor real
- añadir automatización adicional para despliegue o validación