-- Price-change periods for one subscription may not overlap. Multiple
-- distinct subscriptions for one customer remain valid and aggregate.
select a.period_id, b.period_id
from {{ ref('stg_periods') }} a
join {{ ref('stg_periods') }} b
  on a.subscription_id = b.subscription_id and a.period_id < b.period_id
where daterange(a.valid_from, a.valid_to, '[)') &&
      daterange(b.valid_from, b.valid_to, '[)')
