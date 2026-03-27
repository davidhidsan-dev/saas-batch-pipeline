with users as (

    select *
    from {{ ref('dim_users') }}

),

events_by_user as (

    select
        user_id,
        count(*) as total_events,
        min(event_timestamp) as first_event_at,
        max(event_timestamp) as last_event_at
    from {{ ref('fct_events') }}
    group by user_id

),

subscriptions_by_user as (

    select
        user_id,
        count(*) as total_subscriptions,
        countif(is_active_subscription) as active_subscription_count,
        count(*) > 0 as has_subscription
    from {{ ref('fct_subscriptions') }}
    group by user_id

)

select
    u.user_id,
    u.created_at,
    u.signup_date,
    u.country,
    u.acquisition_channel,
    u.plan_type,
    u.is_active,
    u.email_domain,
    u.is_paid_user,
    coalesce(e.total_events, 0) as total_events,
    e.first_event_at,
    e.last_event_at,
    coalesce(s.total_subscriptions, 0) as total_subscriptions,
    coalesce(s.active_subscription_count, 0) as active_subscription_count,
    coalesce(s.has_subscription, false) as has_subscription
from users u
left join events_by_user e
    on u.user_id = e.user_id
left join subscriptions_by_user s
    on u.user_id = s.user_id