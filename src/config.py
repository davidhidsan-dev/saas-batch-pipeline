from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "generated"

# BigQuery
PROJECT_ID = "datasets-490115"
RAW_DATASET = "saas_raw"
STAGING_DATASET = "saas_staging"
MARTS_DATASET = "saas_marts"

# File paths
USERS_FILE = DATA_DIR / "users.csv"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.csv"
EVENTS_FILE = DATA_DIR / "events.csv"

# Synthetic data volumes
USERS_COUNT = 1000
EVENTS_COUNT = 15000

# Reference values
COUNTRIES = ["Spain", "Mexico", "Colombia", "Argentina", "Chile"]
COUNTRY_WEIGHTS = [0.35, 0.25, 0.15, 0.15, 0.10]
ACQUISITION_CHANNELS = ["organic", "paid", "referral"]
ACQUISITION_CHANNELS_WEIGHTS = [0.60, 0.25, 0.15]
PLAN_TYPES = ["free", "basic", "pro"]
PLAN_TYPES_WEIGHTS = [0.75, 0.18, 0.07]
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "company.com", "yahoo.com"]