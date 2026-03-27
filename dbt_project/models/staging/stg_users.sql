select
    user_id,
    created_at,
    country,
    acquisition_channel,
    plan_type,
    is_active,
    email_domain,
    cast(created_at as date) as signup_date
from {{ source('saas_raw', 'users') }}