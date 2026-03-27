select
    event_id,
    user_id,
    event_timestamp,
    cast(event_timestamp as date) as event_date,
    event_type,
    session_id,
    device_type,
    event_value,
    subscription_id
from {{ source('saas_raw', 'events') }}