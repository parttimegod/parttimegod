select * from {{ ref('stg_periods') }}
where extract(day from valid_from) <> 1
   or (valid_to is not null and extract(day from valid_to) <> 1)
