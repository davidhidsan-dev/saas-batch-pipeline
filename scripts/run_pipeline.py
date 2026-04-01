"""
Run the full SaaS batch pipeline end to end.

This script generates synthetic source data, saves local CSV files,
loads raw tables into BigQuery, and executes dbt models and tests.
"""

from pathlib import Path
import subprocess
import sys

from src.config import (
    EVENTS_COUNT,
    EVENTS_FILE,
    SUBSCRIPTIONS_FILE,
    USERS_COUNT,
    USERS_FILE,
)
from src.generate.events_generator import generate_events, save_events
from src.generate.subscriptions_generator import (
    generate_subscriptions,
    save_subscriptions,
)
from src.generate.users_generator import generate_users, save_users
from src.load.bigquery_loader import load_raw_tables_to_bigquery
from src.utils.logger import get_logger

logger = get_logger(__name__)

DBT_PROJECT_DIR = Path(__file__).resolve().parent.parent / "dbt_project"


def run_dbt_command(command: list[str]) -> None:
    """
    Run a dbt command inside the dbt project directory.

    Args:
        command: dbt command to execute as a list of strings.

    Raises:
        RuntimeError: If the dbt command exits with a non-zero status.
    """
    logger.info(f"Running dbt command: {' '.join(command)}")

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_DIR,
        check=False,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"dbt command failed: {' '.join(command)}")


def main() -> None:
    """
    Execute the full batch pipeline from synthetic generation to dbt validation.

    The workflow includes:
    - users generation and local persistence
    - subscriptions generation and local persistence
    - events generation and local persistence
    - raw loading into BigQuery
    - dbt model execution
    - dbt test execution
    """
    logger.info("Starting full batch pipeline")

    logger.info("Generating users dataset")
    users_df = generate_users(USERS_COUNT)
    save_users(users_df, USERS_FILE)
    logger.info(f"Users generated and saved to {USERS_FILE}")

    logger.info("Generating subscriptions dataset")
    subscriptions_df = generate_subscriptions(users_df)
    save_subscriptions(subscriptions_df, SUBSCRIPTIONS_FILE)
    logger.info(f"Subscriptions generated and saved to {SUBSCRIPTIONS_FILE}")

    logger.info("Generating events dataset")
    events_df = generate_events(users_df, subscriptions_df, EVENTS_COUNT)
    save_events(events_df, EVENTS_FILE)
    logger.info(f"Events generated and saved to {EVENTS_FILE}")

    logger.info("Loading raw tables into BigQuery")
    load_raw_tables_to_bigquery()

    logger.info("Running dbt models")
    run_dbt_command(["dbt", "run"])

    logger.info("Running dbt tests")
    run_dbt_command(["dbt", "test"])

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception(f"Pipeline failed: {exc}")
        sys.exit(1)