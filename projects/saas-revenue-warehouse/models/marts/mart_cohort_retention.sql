-- Denominator: cohort's starting paid customers; an observed zero stays zero.
-- Calendar stops at the as-of date: future/unobserved cells are absent.
with size as (
    select cohort_month, count(*) as cohort_size
    from {{ ref('int_customer_month') }}
    where month = cohort_month and mrr > 0
    group by cohort_month
)
select c.cohort_month, c.month,
       ((extract(year from c.month) - extract(year from c.cohort_month)) * 12
        + extract(month from c.month) - extract(month from c.cohort_month))::int
           as months_since_signup,
       s.cohort_size,
       count(*) filter (where c.mrr > 0) as retained_customers,
       count(*) filter (where c.mrr > 0)::numeric / s.cohort_size as retention_rate
from {{ ref('int_customer_month') }} c
join size s using (cohort_month)
where c.month >= c.cohort_month
group by c.cohort_month, c.month, s.cohort_size
