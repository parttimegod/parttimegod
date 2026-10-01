-- dbt fails when any returned row violates the revenue identity.
select * from {{ ref('mart_monthly_revenue') }}
where mrr <> opening_mrr + new_mrr + reactivation_mrr + expansion_mrr
             - contraction_mrr - churn_mrr
