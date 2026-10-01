-- The opening snapshot is only known when the calendar includes signup history.
select min(valid_from) as first_subscription
from {{ ref('stg_periods') }}
having min(valid_from) < (select min(month) from {{ source('raw', 'calendar') }})
    or not exists (select 1 from {{ source('raw', 'calendar') }})
