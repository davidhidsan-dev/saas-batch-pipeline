# Data Model / Modelo de Datos

## ES — Objetivo del modelo

Este proyecto simula una fuente operativa sencilla de tipo SaaS para construir un pipeline batch reproducible con Python, BigQuery y dbt.

Los datos son sintéticos, pero siguen relaciones coherentes entre usuarios, eventos y suscripciones. El objetivo no es modelar un negocio SaaS perfecto, sino disponer de una base suficientemente realista para practicar ingestión, modelado por capas, transformación SQL y validación de calidad.

## ES — Datasets en BigQuery

El proyecto utiliza tres datasets en BigQuery:

- `saas_raw`
- `saas_staging`
- `saas_marts`

En este proyecto:

- `saas_raw` contiene los datos generados con Python y cargados con mínima intervención
- `saas_staging` contiene modelos dbt de limpieza, tipado y estandarización
- `saas_marts` contiene modelos dbt finales listos para consumo analítico

Esta separación permite distinguir claramente entre ingestión, transformación intermedia y capa final de consumo.

## ES — Tabla raw `users`

La tabla `users` representa los usuarios del producto.

Columnas propuestas:

- `user_id` (STRING): identificador único del usuario
- `created_at` (TIMESTAMP): timestamp de alta del usuario
- `country` (STRING): país del usuario
- `acquisition_channel` (STRING): canal de adquisición
- `plan_type` (STRING): tipo de plan actual, por ejemplo `free`, `basic`, `pro`
- `is_active` (BOOLEAN): indicador de actividad actual
- `email_domain` (STRING): dominio de email sintético

En este proyecto:

- existe una fila por usuario
- un usuario se crea una sola vez
- no todos los usuarios están activos
- la distribución de países, canales y planes no debe ser uniforme

## ES — Tabla raw `subscriptions`

La tabla `subscriptions` representa las suscripciones de pago.

Columnas propuestas:

- `subscription_id` (STRING): identificador único de la suscripción
- `user_id` (STRING): identificador del usuario
- `start_date` (DATE): fecha de inicio
- `end_date` (DATE): fecha de fin, nullable si sigue activa
- `billing_cycle` (STRING): ciclo de facturación, por ejemplo `monthly` o `yearly`
- `price_amount` (FLOAT): importe de la suscripción
- `status` (STRING): estado, por ejemplo `active`, `canceled`, `expired`
- `plan_tier` (STRING): nivel del plan, por ejemplo `basic` o `pro`

En este proyecto:

- no todos los usuarios tienen suscripción
- en esta primera versión del proyecto, un usuario puede tener como máximo una suscripción
- una suscripción activa normalmente tendrá `end_date` nulo
- las suscripciones se generan a partir de usuarios con plan de pago

## ES — Tabla raw `events`

La tabla `events` representa eventos de uso del producto.

Columnas propuestas:

- `event_id` (STRING): identificador único del evento
- `user_id` (STRING): identificador del usuario
- `event_timestamp` (TIMESTAMP): timestamp del evento
- `event_type` (STRING): tipo de evento, por ejemplo `page_view`, `login`, `feature_use`, `upgrade_click`, `cancel_click`
- `session_id` (STRING): identificador sintético de sesión
- `device_type` (STRING): tipo de dispositivo, por ejemplo `web`, `mobile`, `tablet`
- `event_value` (FLOAT): valor numérico opcional para algunos eventos
- `subscription_id` (STRING): identificador de suscripción relacionado, nullable

En este proyecto:

- un usuario puede tener muchos eventos
- todo evento debe pertenecer a un usuario existente
- algunos eventos pueden relacionarse con una suscripción y otros no
- la distribución de eventos por usuario no debe ser uniforme

## ES — Relaciones entre tablas

El modelo define las siguientes relaciones:

- `users.user_id` → `events.user_id`
- `users.user_id` → `subscriptions.user_id`
- `subscriptions.subscription_id` → `events.subscription_id` como relación opcional

Esto implica que:

- un usuario puede tener muchos eventos
- en esta primera versión del proyecto, un usuario puede tener cero o una suscripción
- una suscripción puede estar asociada a uno o varios eventos relacionados
- algunos eventos no tendrán suscripción asociada

## ES — Reglas de coherencia de la fuente sintética

Los datos generados deben seguir estas reglas mínimas de coherencia:

- todo `events.user_id` debe existir en `users.user_id`
- todo `subscriptions.user_id` debe existir en `users.user_id`
- `events.event_timestamp` debe ser mayor o igual que `users.created_at`
- `subscriptions.start_date` debe ser mayor o igual que `DATE(users.created_at)`
- no todos los usuarios deben tener el mismo número de eventos
- no todos los usuarios deben tener suscripción
- si `subscriptions.status = 'active'`, `end_date` será normalmente nulo
- si `subscriptions.status` es `canceled` o `expired`, `end_date` debería existir en la mayoría de casos
- `events.subscription_id` puede ser nulo para eventos no relacionados con pagos
- las distribuciones de `country`, `acquisition_channel`, `plan_type` y `event_type` no deben ser uniformes

Estas reglas no buscan perfección absoluta, sino consistencia suficiente para un pipeline de data engineering.

## ES — Volumen inicial del MVP

El volumen inicial recomendado para el MVP es:

- `users`: 1.000 filas
- `subscriptions`: aproximadamente 180 a 230 filas, dependiendo de la distribución generada de usuarios de pago
- `events`: 12.000 a 20.000 filas

Este volumen es suficiente para:

- probar joins
- construir modelos staging y marts
- ejecutar tests de calidad
- validar la reproducibilidad del pipeline

sin añadir complejidad innecesaria.

## ES — Implicaciones para el modelado posterior

La capa raw debe conservar la estructura de la fuente sintética con cambios mínimos.

En este proyecto:

- Python se usa para generar y cargar datos
- dbt se usa para transformar y testear datos
- la lógica principal de transformación debe vivir en SQL y dbt, no en Python

Esto significa que:

- `saas_raw` conserva los datos casi tal como se generan
- `saas_staging` limpia, tipa y estandariza
- `saas_marts` expone modelos finales simples y explicables

---

## EN — Model objective

This project simulates a simple SaaS operational source in order to build a reproducible batch pipeline with Python, BigQuery and dbt.

The data is synthetic, but it follows coherent relationships between users, events and subscriptions. The goal is not to model a perfect SaaS business, but to create a realistic enough base to practice ingestion, layered modeling, SQL transformations and data quality validation.

## EN — BigQuery datasets

The project uses three BigQuery datasets:

- `saas_raw`
- `saas_staging`
- `saas_marts`

In this project:

- `saas_raw` contains Python-generated data loaded with minimal intervention
- `saas_staging` contains dbt models for cleaning, typing and standardization
- `saas_marts` contains final dbt models ready for analytical consumption

This separation makes it easier to distinguish ingestion, intermediate transformation and final consumption layers.

## EN — Raw table `users`

The `users` table represents product users.

Proposed columns:

- `user_id` (STRING): unique user identifier
- `created_at` (TIMESTAMP): user signup timestamp
- `country` (STRING): user country
- `acquisition_channel` (STRING): acquisition source
- `plan_type` (STRING): current plan type, for example `free`, `basic`, `pro`
- `is_active` (BOOLEAN): current activity flag
- `email_domain` (STRING): synthetic email domain

In this project:

- there is one row per user
- a user is created once
- not all users are active
- country, acquisition channel and plan distributions should not be uniform

## EN — Raw table `subscriptions`

The `subscriptions` table represents paid subscriptions.

Proposed columns:

- `subscription_id` (STRING): unique subscription identifier
- `user_id` (STRING): user identifier
- `start_date` (DATE): subscription start date
- `end_date` (DATE): subscription end date, nullable if still active
- `billing_cycle` (STRING): billing cycle, for example `monthly` or `yearly`
- `price_amount` (FLOAT): subscription amount
- `status` (STRING): status, for example `active`, `canceled`, `expired`
- `plan_tier` (STRING): plan tier, for example `basic` or `pro`

In this project:

- not all users have a subscription
- in this first version of the project, one user can have at most one subscription
- an active subscription will usually have a null `end_date`
- subscriptions are generated from paid users

## EN — Raw table `events`

The `events` table represents product usage events.

Proposed columns:

- `event_id` (STRING): unique event identifier
- `user_id` (STRING): user identifier
- `event_timestamp` (TIMESTAMP): event timestamp
- `event_type` (STRING): event type, for example `page_view`, `login`, `feature_use`, `upgrade_click`, `cancel_click`
- `session_id` (STRING): synthetic session identifier
- `device_type` (STRING): device type, for example `web`, `mobile`, `tablet`
- `event_value` (FLOAT): optional numeric value for some events
- `subscription_id` (STRING): related subscription identifier, nullable

In this project:

- one user can have many events
- every event must belong to an existing user
- some events may be related to a subscription and some may not
- event distribution across users should not be uniform

## EN — Table relationships

The model defines the following relationships:

- `users.user_id` → `events.user_id`
- `users.user_id` → `subscriptions.user_id`
- `subscriptions.subscription_id` → `events.subscription_id` as an optional relationship

This implies that:

- one user can have many events
- in this first version of the project, one user can have zero or one subscription
- one subscription can be associated with one or more related events
- some events will not have an associated subscription

## EN — Synthetic source consistency rules

The generated data should follow these minimum consistency rules:

- every `events.user_id` must exist in `users.user_id`
- every `subscriptions.user_id` must exist in `users.user_id`
- `events.event_timestamp` must be greater than or equal to `users.created_at`
- `subscriptions.start_date` must be greater than or equal to `DATE(users.created_at)`
- not all users should have the same number of events
- not all users should have a subscription
- if `subscriptions.status = 'active'`, `end_date` will usually be null
- if `subscriptions.status` is `canceled` or `expired`, `end_date` should exist in most cases
- `events.subscription_id` can be null for non-payment-related events
- `country`, `acquisition_channel`, `plan_type` and `event_type` distributions should not be uniform

These rules are not meant to achieve perfect realism, but to provide enough consistency for a data engineering pipeline.

## EN — Initial MVP volume

The recommended initial MVP volume is:

- `users`: 1,000 rows
- `subscriptions`: approximately 180 to 230 rows, depending on the generated distribution of paid users
- `events`: 12,000 to 20,000 rows

This volume is enough to:

- test joins
- build staging and marts models
- run data quality tests
- validate pipeline reproducibility

without adding unnecessary complexity.

## EN — Implications for downstream modeling

The raw layer should preserve the structure of the synthetic source with minimal changes.

In this project:

- Python is used to generate and load data
- dbt is used to transform and test data
- the main transformation logic should live in SQL and dbt, not in Python

This means that:

- `saas_raw` keeps the data almost as generated
- `saas_staging` cleans, casts and standardizes
- `saas_marts` exposes final models that are simple and explainable