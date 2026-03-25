from src.config import USERS_COUNT, USERS_FILE, SUBSCRIPTIONS_FILE
from src.generate.users_generator import generate_users, save_users
from src.generate.subscriptions_generator import generate_subscriptions, save_subscriptions


def main() -> None:
    users_df = generate_users(USERS_COUNT)
    subscriptions_df = generate_subscriptions(users_df)

    save_users(users_df, USERS_FILE)
    save_subscriptions(subscriptions_df, SUBSCRIPTIONS_FILE)

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

    user_ids_exist = subscriptions_df["user_id"].isin(users_df["user_id"]).all()
    print(f"All subscription user_id exist in users: {user_ids_exist}")

    free_user_ids = set(users_df.loc[users_df["plan_type"] == "free", "user_id"])
    free_users_in_subscriptions = subscriptions_df["user_id"].isin(free_user_ids).any()
    print(f"Any free users in subscriptions: {free_users_in_subscriptions}")

    active_with_end_date = subscriptions_df.loc[
        subscriptions_df["status"] == "active", "end_date"
    ].notna().any()
    print(f"Any active subscriptions with end_date: {active_with_end_date}")


if __name__ == "__main__":
    main()