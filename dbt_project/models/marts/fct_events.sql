select
    event_id,
    user_id,
    event_timestamp,
    event_date,
    event_type,
    session_id,
    device_type,
    event_value,
    subscription_id,
    case
        when subscription_id is not null then true
        else false
    end as is_subscription_event
from {{ ref('stg_events') }}