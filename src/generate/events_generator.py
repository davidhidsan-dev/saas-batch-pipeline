"""
Generate synthetic SaaS events data for the batch pipeline.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def generate_events(
    users_df: pd.DataFrame,
    subscriptions_df: pd.DataFrame,
    n_events: int,
) -> pd.DataFrame:
    """
    Generate a synthetic events dataset for the SaaS source model.

    Events are generated from existing users and may optionally reference
    a subscription for payment-related event types. The dataset includes
    timestamps, event types, session identifiers, device types, and
    optional numeric values for selected events.

    Args:
        users_df: Users dataframe used as the source for event generation.
        subscriptions_df: Subscriptions dataframe used to map users to subscriptions.
        n_events: Number of events to generate.

    Returns:
        DataFrame with synthetic events data.
    """
    event_ids = []
    user_ids = []
    event_timestamps = []
    event_types = []
    session_ids = []
    device_types = []
    event_values = []
    subscription_ids = []

    event_type_options = [
        "page_view",
        "feature_use",
        "login",
        "upgrade_click",
        "cancel_click",
    ]
    event_type_weights = [0.45, 0.30, 0.20, 0.03, 0.02]

    device_type_options = ["web", "mobile", "tablet"]
    device_type_weights = [0.60, 0.35, 0.05]

    user_subscription_map = (
        subscriptions_df.drop_duplicates(subset=["user_id"])
        .set_index("user_id")["subscription_id"]
        .to_dict()
    )

    users_records = list(
        users_df[["user_id", "created_at"]].itertuples(index=False, name=None)
    )
    now = datetime.now()

    for i in range(1, n_events + 1):
        user_id, created_at = random.choice(users_records)

        max_seconds_after_signup = max(
            1,
            int((now - created_at).total_seconds())
        )
        random_seconds_after_signup = random.randint(0, max_seconds_after_signup)
        event_timestamp = created_at + timedelta(seconds=random_seconds_after_signup)

        event_type = random.choices(
            event_type_options,
            weights=event_type_weights,
            k=1,
        )[0]

        device_type = random.choices(
            device_type_options,
            weights=device_type_weights,
            k=1,
        )[0]

        session_id = f"session_{random.randint(1, n_events // 2):05d}"

        subscription_id = None
        if event_type in ["upgrade_click", "cancel_click"]:
            subscription_id = user_subscription_map.get(user_id)

        event_value = None
        if event_type == "feature_use":
            event_value = float(random.randint(1, 5))

        event_ids.append(f"event_{i:05d}")
        user_ids.append(user_id)
        event_timestamps.append(event_timestamp)
        event_types.append(event_type)
        session_ids.append(session_id)
        device_types.append(device_type)
        event_values.append(event_value)
        subscription_ids.append(subscription_id)

    df = pd.DataFrame(
        {
            "event_id": event_ids,
            "user_id": user_ids,
            "event_timestamp": event_timestamps,
            "event_type": event_types,
            "session_id": session_ids,
            "device_type": device_types,
            "event_value": event_values,
            "subscription_id": subscription_ids,
        }
    )

    return df


def save_events(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the generated events dataset to a CSV file.

    Args:
        df: Events dataframe to save.
        output_path: Destination path for the CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)