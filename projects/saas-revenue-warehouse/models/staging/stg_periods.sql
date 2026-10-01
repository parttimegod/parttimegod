select period_id, customer_id, subscription_id, valid_from, valid_to,
       monthly_price
from {{ source('raw', 'subscription_period') }}
