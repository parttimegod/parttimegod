select month,
       sum(mrr) as mrr, sum(prior_mrr) as opening_mrr,
       count(*) filter (where mrr > 0) as active_customers,
       sum(new_mrr) as new_mrr, sum(reactivation_mrr) as reactivation_mrr,
       sum(expansion_mrr) as expansion_mrr,
       sum(contraction_mrr) as contraction_mrr, sum(churn_mrr) as churn_mrr,
       (sum(prior_mrr) + sum(expansion_mrr) - sum(contraction_mrr)
        - sum(churn_mrr)) / nullif(sum(prior_mrr), 0) as net_revenue_retention,
       sum(churn_mrr) / nullif(sum(prior_mrr), 0) as revenue_churn_rate,
       count(*) filter (where prior_mrr > 0 and mrr = 0)::numeric /
       nullif(count(*) filter (where prior_mrr > 0), 0) as customer_churn_rate
from {{ ref('fct_mrr_movements') }}
group by month
