select customer_id, month from {{ ref('int_customer_month') }}
group by customer_id, month having count(*) <> 1
