select
    subscription_id,
    user_id,
    start_date,
    end_date,
    billing_cycle,
    price_amount,
    status,
    plan_tier,
    case
        when status = 'active' then true
        else false
    end as is_active_subscription,
    case
        when end_date is not null then date_diff(end_date, start_date, day)
        else null
    end as subscription_length_days
from {{ ref('stg_subscriptions') }}