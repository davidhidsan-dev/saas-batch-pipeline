from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

from airflow.decorators import dag, task

PROJECT_ROOT = Path("/mnt/c/Users/Usuario/Documents/Proyectos/saas-batch-pipeline")
WINDOWS_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
WINDOWS_DBT = PROJECT_ROOT / ".venv" / "Scripts" / "dbt.exe"
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt_project"


def run_subprocess(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )
    return result


@dag(
    dag_id="saas_batch_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["saas", "batch", "bigquery", "dbt", "airflow"],
)
def saas_batch_pipeline():
    @task
    def generate_users() -> dict:
        code = """
import json
from src.config import USERS_COUNT, USERS_FILE
from src.generate.users_generator import generate_users, save_users

df = generate_users(USERS_COUNT)
save_users(df, USERS_FILE)

print(json.dumps({
    "csv_path": str(USERS_FILE),
    "row_count": int(len(df))
}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def generate_subscriptions(users_output: dict) -> dict:
        code = f"""
import json
import pandas as pd
from pathlib import Path
from src.config import SUBSCRIPTIONS_FILE
from src.generate.subscriptions_generator import generate_subscriptions, save_subscriptions

users_path = Path(r"{users_output["csv_path"]}")
users_df = pd.read_csv(users_path, parse_dates=["created_at"])

df = generate_subscriptions(users_df)
save_subscriptions(df, SUBSCRIPTIONS_FILE)

print(json.dumps({{
    "csv_path": str(SUBSCRIPTIONS_FILE),
    "row_count": int(len(df))
}}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def generate_events(users_output: dict, subscriptions_output: dict) -> dict:
        code = f"""
import json
import pandas as pd
from pathlib import Path
from src.config import EVENTS_COUNT, EVENTS_FILE
from src.generate.events_generator import generate_events, save_events

users_path = Path(r"{users_output["csv_path"]}")
subscriptions_path = Path(r"{subscriptions_output["csv_path"]}")

users_df = pd.read_csv(users_path, parse_dates=["created_at"])
subscriptions_df = pd.read_csv(subscriptions_path)

df = generate_events(users_df, subscriptions_df, EVENTS_COUNT)
save_events(df, EVENTS_FILE)

print(json.dumps({{
    "csv_path": str(EVENTS_FILE),
    "row_count": int(len(df))
}}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def load_raw_users(users_output: dict) -> dict:
        code = f"""
import json
from pathlib import Path
from src.load.bigquery_loader import USERS_SCHEMA, load_csv_to_bigquery

table_id = load_csv_to_bigquery(
    csv_path=Path(r"{users_output["csv_path"]}"),
    table_name="users",
    schema=USERS_SCHEMA,
)

print(json.dumps({{
    "table_id": table_id
}}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def load_raw_subscriptions(subscriptions_output: dict) -> dict:
        code = f"""
import json
from pathlib import Path
from src.load.bigquery_loader import SUBSCRIPTIONS_SCHEMA, load_csv_to_bigquery

table_id = load_csv_to_bigquery(
    csv_path=Path(r"{subscriptions_output["csv_path"]}"),
    table_name="subscriptions",
    schema=SUBSCRIPTIONS_SCHEMA,
)

print(json.dumps({{
    "table_id": table_id
}}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def load_raw_events(events_output: dict) -> dict:
        code = f"""
import json
from pathlib import Path
from src.load.bigquery_loader import EVENTS_SCHEMA, load_csv_to_bigquery

table_id = load_csv_to_bigquery(
    csv_path=Path(r"{events_output["csv_path"]}"),
    table_name="events",
    schema=EVENTS_SCHEMA,
)

print(json.dumps({{
    "table_id": table_id
}}))
"""
        result = run_subprocess(
            [str(WINDOWS_PYTHON), "-c", code],
            cwd=PROJECT_ROOT,
        )
        return json.loads(result.stdout.strip().splitlines()[-1])

    @task
    def dbt_run_staging() -> None:
        run_subprocess(
            [str(WINDOWS_DBT), "run", "--select", "staging"],
            cwd=DBT_PROJECT_DIR,
        )

    @task
    def dbt_run_marts() -> None:
        run_subprocess(
            [str(WINDOWS_DBT), "run", "--select", "marts"],
            cwd=DBT_PROJECT_DIR,
        )

    @task
    def dbt_test() -> None:
        run_subprocess(
            [str(WINDOWS_DBT), "test"],
            cwd=DBT_PROJECT_DIR,
        )

    users_output = generate_users()
    subscriptions_output = generate_subscriptions(users_output)
    events_output = generate_events(users_output, subscriptions_output)

    load_users = load_raw_users(users_output)
    load_subscriptions = load_raw_subscriptions(subscriptions_output)
    load_events = load_raw_events(events_output)

    staging = dbt_run_staging()
    marts = dbt_run_marts()
    tests = dbt_test()

    load_users >> staging
    load_subscriptions >> staging
    load_events >> staging
    staging >> marts >> tests


saas_batch_pipeline()