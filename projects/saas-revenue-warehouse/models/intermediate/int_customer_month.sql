-- Grain: one customer per calendar month, including inactive months.
-- The spine prevents LAG from skipping a cancellation/return month.
with cohort as (
    select customer_id, date_trunc('month', min(valid_from))::date as cohort_month
    from {{ ref('stg_periods') }}
    group by customer_id
), snapshot as (
    select c.customer_id, m.month, co.cohort_month, c.segment, c.country,
           coalesce(sum(p.monthly_price), 0)::numeric(12,2) as mrr
    from {{ source('raw', 'customer') }} c
    cross join {{ source('raw', 'calendar') }} m
    join cohort co on co.customer_id = c.customer_id
    left join {{ ref('stg_periods') }} p
        on p.customer_id = c.customer_id
       and p.valid_from <= m.month
       and (p.valid_to is null or m.month < p.valid_to)
    group by c.customer_id, m.month, co.cohort_month, c.segment, c.country
)
select *, lag(mrr, 1, 0::numeric) over
    (partition by customer_id order by month) as prior_mrr
from snapshot
