select
    user_id,
    created_at,
    signup_date,
    country,
    acquisition_channel,
    plan_type,
    is_active,
    email_domain,
    case
        when plan_type in ('basic', 'pro') then true
        else false
    end as is_paid_user
from {{ ref('stg_users') }}