"""
Load synthetic SaaS source tables from local CSV files into BigQuery raw tables.
"""

from pathlib import Path

import pandas as pd
from google.cloud import bigquery

from src.config import (
    EVENTS_FILE,
    PROJECT_ID,
    RAW_DATASET,
    SUBSCRIPTIONS_FILE,
    USERS_FILE,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


USERS_SCHEMA = [
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("acquisition_channel", "STRING"),
    bigquery.SchemaField("plan_type", "STRING"),
    bigquery.SchemaField("is_active", "BOOL"),
    bigquery.SchemaField("email_domain", "STRING"),
]

SUBSCRIPTIONS_SCHEMA = [
    bigquery.SchemaField("subscription_id", "STRING"),
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("start_date", "DATE"),
    bigquery.SchemaField("end_date", "DATE"),
    bigquery.SchemaField("billing_cycle", "STRING"),
    bigquery.SchemaField("price_amount", "FLOAT"),
    bigquery.SchemaField("status", "STRING"),
    bigquery.SchemaField("plan_tier", "STRING"),
]

EVENTS_SCHEMA = [
    bigquery.SchemaField("event_id", "STRING"),
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("event_timestamp", "TIMESTAMP"),
    bigquery.SchemaField("event_type", "STRING"),
    bigquery.SchemaField("session_id", "STRING"),
    bigquery.SchemaField("device_type", "STRING"),
    bigquery.SchemaField("event_value", "FLOAT"),
    bigquery.SchemaField("subscription_id", "STRING"),
]


def ensure_dataset_exists(client: bigquery.Client, dataset_name: str) -> None:
    """
    Create a BigQuery dataset if it does not already exist.

    Args:
        client: Initialized BigQuery client.
        dataset_name: Name of the dataset to check or create.
    """
    dataset_id = f"{PROJECT_ID}.{dataset_name}"

    try:
        client.get_dataset(dataset_id)
        logger.info(f"BigQuery dataset already exists dataset={dataset_id}")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        client.create_dataset(dataset)
        logger.info(f"BigQuery dataset created dataset={dataset_id}")


def load_csv_to_bigquery(
    csv_path: Path,
    table_name: str,
    schema: list[bigquery.SchemaField],
) -> str:
    """
    Load a local CSV file into a BigQuery raw table.

    Args:
        csv_path: Path to the source CSV file.
        table_name: Target BigQuery table name.
        schema: Explicit BigQuery schema for the target table.

    Returns:
        Fully qualified BigQuery table id.

    Raises:
        ValueError: If PROJECT_ID is not configured in the environment.
    """
    if not PROJECT_ID:
        raise ValueError("PROJECT_ID is not set in the environment variables.")

    logger.info(f"Reading local CSV file path={csv_path}")

    df = pd.read_csv(csv_path)

    table_id = f"{PROJECT_ID}.{RAW_DATASET}.{table_name}"
    logger.info(f"Preparing BigQuery load table={table_id} rows={len(df)}")

    if df.empty:
        logger.warning(f"CSV is empty before BigQuery load table={table_id}")

    client = bigquery.Client(project=PROJECT_ID)
    ensure_dataset_exists(client, RAW_DATASET)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE",
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )

    with open(csv_path, "rb") as file_obj:
        job = client.load_table_from_file(
            file_obj,
            table_id,
            job_config=job_config,
        )

    job.result()

    logger.info(f"BigQuery load completed table={table_id}")

    return table_id


def load_raw_tables_to_bigquery() -> None:
    """
    Load all generated raw source tables into BigQuery.

    This includes the users, subscriptions, and events source tables.
    """
    users_table_id = load_csv_to_bigquery(
        csv_path=USERS_FILE,
        table_name="users",
        schema=USERS_SCHEMA,
    )

    subscriptions_table_id = load_csv_to_bigquery(
        csv_path=SUBSCRIPTIONS_FILE,
        table_name="subscriptions",
        schema=SUBSCRIPTIONS_SCHEMA,
    )

    events_table_id = load_csv_to_bigquery(
        csv_path=EVENTS_FILE,
        table_name="events",
        schema=EVENTS_SCHEMA,
    )

    client = bigquery.Client(project=PROJECT_ID)

    users_table = client.get_table(users_table_id)
    subscriptions_table = client.get_table(subscriptions_table_id)
    events_table = client.get_table(events_table_id)

    logger.info(f"Loaded {users_table.num_rows} rows into {users_table_id}")
    logger.info(
        f"Loaded {subscriptions_table.num_rows} rows into {subscriptions_table_id}"
    )
    logger.info(f"Loaded {events_table.num_rows} rows into {events_table_id}")


def main() -> None:
    """
    Load all generated raw source tables into BigQuery.
    """
    load_raw_tables_to_bigquery()


if __name__ == "__main__":
    main()