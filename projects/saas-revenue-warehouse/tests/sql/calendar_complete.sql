-- LAG assumes consecutive months, including months with no paying customers.
with bounds as (
    select min(month) as first_month, max(month) as last_month
    from {{ source('raw', 'calendar') }}
), expected as (
    select d::date as month
    from bounds
    cross join lateral generate_series(first_month, last_month, '1 month') d
)
select e.month
from expected e
left join {{ source('raw', 'calendar') }} c using (month)
where c.month is null
