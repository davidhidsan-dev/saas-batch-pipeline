import random
from pathlib import Path
from datetime import timedelta

import pandas as pd


def generate_subscriptions(users_df: pd.DataFrame) -> pd.DataFrame:
    """Generate synthetic SaaS subscriptions from paid users."""
    max_days_start = 30
    min_days_end = 30
    max_days_end = 180

    paid_users_df = users_df[users_df["plan_type"].isin(["basic", "pro"])].copy()

    if paid_users_df.empty:
        return pd.DataFrame(
            columns=[
                "subscription_id",
                "user_id",
                "start_date",
                "end_date",
                "billing_cycle",
                "price_amount",
                "status",
                "plan_tier",
            ]
        )

    n_subscriptions = max(1, int(len(paid_users_df) * 0.85))
    selected_users_df = paid_users_df.sample(n=n_subscriptions, random_state=42)

    subscription_ids = []
    user_ids = []
    start_dates = []
    end_dates = []
    billing_cycles = []
    price_amounts = []
    statuses = []
    plan_tiers = []

    subscription_counter = 1

    for user in selected_users_df.itertuples(index=False):
        subscription_ids.append(f"sub_{subscription_counter:04d}")
        user_ids.append(user.user_id)

        start_day = user.created_at + timedelta(days=random.randint(0, max_days_start))
        start_dates.append(start_day.date())

        plan_tier = user.plan_type
        plan_tiers.append(plan_tier)

        billing_cycle = random.choices(
            ["monthly", "yearly"],
            weights=[0.80, 0.20],
            k=1,
        )[0]
        billing_cycles.append(billing_cycle)

        if plan_tier == "basic":
            price = 29.0 if billing_cycle == "monthly" else 290.0
        else:
            price = 79.0 if billing_cycle == "monthly" else 790.0

        price_amounts.append(price)

        status = random.choices(
            ["active", "canceled", "expired"],
            weights=[0.70, 0.20, 0.10],
            k=1,
        )[0]
        statuses.append(status)

        if status == "active":
            end_day = None
        else:
            end_day = start_day + timedelta(days=random.randint(min_days_end, max_days_end))
            end_day = end_day.date()

        end_dates.append(end_day)

        subscription_counter += 1

    df = pd.DataFrame(
        {
            "subscription_id": subscription_ids,
            "user_id": user_ids,
            "start_date": start_dates,
            "end_date": end_dates,
            "billing_cycle": billing_cycles,
            "price_amount": price_amounts,
            "status": statuses,
            "plan_tier": plan_tiers,
        }
    )

    return df


def save_subscriptions(df: pd.DataFrame, output_path: Path) -> None:
    """Save subscriptions dataframe to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)