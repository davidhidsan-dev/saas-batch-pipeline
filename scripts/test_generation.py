import pandas as pd

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


def main() -> None:
    users_df = generate_users(USERS_COUNT)
    subscriptions_df = generate_subscriptions(users_df)
    events_df = generate_events(users_df, subscriptions_df, EVENTS_COUNT)

    save_users(users_df, USERS_FILE)
    save_subscriptions(subscriptions_df, SUBSCRIPTIONS_FILE)
    save_events(events_df, EVENTS_FILE)

    print("=== USERS ===")
    print(f"Rows: {len(users_df)}")
    print(f"Unique user_id: {users_df['user_id'].nunique()}")
    print(users_df.head())
    print()
    print(users_df["plan_type"].value_counts())
    print()

    print("=== SUBSCRIPTIONS ===")
    print(f"Rows: {len(subscriptions_df)}")
    print(f"Unique subscription_id: {subscriptions_df['subscription_id'].nunique()}")
    print(subscriptions_df.head())
    print()

    subscription_user_ids_exist = subscriptions_df["user_id"].isin(users_df["user_id"]).all()
    print(f"All subscription user_id exist in users: {subscription_user_ids_exist}")

    free_user_ids = set(users_df.loc[users_df["plan_type"] == "free", "user_id"])
    free_users_in_subscriptions = subscriptions_df["user_id"].isin(free_user_ids).any()
    print(f"Any free users in subscriptions: {free_users_in_subscriptions}")

    active_with_end_date = subscriptions_df.loc[
        subscriptions_df["status"] == "active", "end_date"
    ].notna().any()
    print(f"Any active subscriptions with end_date: {active_with_end_date}")

    today = pd.Timestamp.today().normalize().date()

    future_subscription_start = (
        pd.to_datetime(subscriptions_df["start_date"]).dt.date > today
    ).any()
    print(f"Any subscription start_date in the future: {future_subscription_start}")

    future_subscription_end = (
        pd.to_datetime(subscriptions_df["end_date"], errors="coerce").dt.date > today
    ).any()
    print(f"Any subscription end_date in the future: {future_subscription_end}")
    print()

    print("=== EVENTS ===")
    print(f"Rows: {len(events_df)}")
    print(f"Unique event_id: {events_df['event_id'].nunique()}")
    print(events_df.head())
    print()

    event_user_ids_exist = events_df["user_id"].isin(users_df["user_id"]).all()
    print(f"All event user_id exist in users: {event_user_ids_exist}")

    event_subscription_ids_exist = (
        events_df["subscription_id"].dropna().isin(subscriptions_df["subscription_id"]).all()
    )
    print(
        "All non-null event subscription_id exist in subscriptions: "
        f"{event_subscription_ids_exist}"
    )


if __name__ == "__main__":
    main()