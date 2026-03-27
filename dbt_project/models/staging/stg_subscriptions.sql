select
    subscription_id,
    user_id,
    start_date,
    end_date,
    billing_cycle,
    price_amount,
    status,
    plan_tier
from {{ source('saas_raw', 'subscriptions') }}