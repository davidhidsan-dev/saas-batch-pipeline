import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from src.config import (
    ACQUISITION_CHANNELS,
    ACQUISITION_CHANNELS_WEIGHTS,
    COUNTRIES,
    COUNTRY_WEIGHTS,
    EMAIL_DOMAINS,
    PLAN_TYPES,
    PLAN_TYPES_WEIGHTS,
)


def generate_users(n_users: int) -> pd.DataFrame:
    """Generate synthetic SaaS users."""
    now = datetime.now()
    max_seconds_back = 365 * 24 * 60 * 60

    user_ids = []
    created_at_values = []
    countries = []
    acquisition_channels = []
    plan_types = []
    is_active_values = []
    email_domains = []

    for i in range(1, n_users + 1):
        user_ids.append(f"user_{i:04d}")

        random_seconds_back = random.randint(0, max_seconds_back)
        created_at = now - timedelta(seconds=random_seconds_back)
        created_at_values.append(created_at)

        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        countries.append(country)

        acquisition = random.choices(
            ACQUISITION_CHANNELS,
            weights=ACQUISITION_CHANNELS_WEIGHTS,
            k=1,
        )[0]
        acquisition_channels.append(acquisition)

        plan = random.choices(PLAN_TYPES, weights=PLAN_TYPES_WEIGHTS, k=1)[0]
        plan_types.append(plan)

        active = random.choices([True, False], weights=[0.8, 0.2], k=1)[0]
        is_active_values.append(active)

        email = random.choice(EMAIL_DOMAINS)
        email_domains.append(email)

    df = pd.DataFrame(
        {
            "user_id": user_ids,
            "created_at": created_at_values,
            "country": countries,
            "acquisition_channel": acquisition_channels,
            "plan_type": plan_types,
            "is_active": is_active_values,
            "email_domain": email_domains,
        }
    )

    return df


def save_users(df: pd.DataFrame, output_path: Path) -> None:
    """Save users dataframe to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)