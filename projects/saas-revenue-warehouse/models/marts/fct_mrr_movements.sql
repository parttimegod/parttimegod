-- Movement classification reconciles the change in recurring revenue.
select *,
    case when mrr > 0 and prior_mrr = 0 and month = cohort_month
         then mrr else 0 end as new_mrr,
    case when mrr > 0 and prior_mrr = 0 and month > cohort_month
         then mrr else 0 end as reactivation_mrr,
    case when prior_mrr > 0 and mrr > prior_mrr
         then mrr - prior_mrr else 0 end as expansion_mrr,
    case when mrr > 0 and mrr < prior_mrr
         then prior_mrr - mrr else 0 end as contraction_mrr,
    case when mrr = 0 and prior_mrr > 0
         then prior_mrr else 0 end as churn_mrr
from {{ ref('int_customer_month') }}
