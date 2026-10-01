# Model notes

## Customer-month grain

A customer can have several subscriptions. The period join adds prices
together before counting customers or calculating movements. Otherwise
two subscriptions would make one customer appear twice in retention.

The fixture includes this case: A pays $60 on one subscription and $40
on another in January. The total is $100 and the customer count is one.

## Calendar before LAG

Working only with active subscriptions would remove inactive months.
For a customer paying in January, absent in February and returning in
March, LAG would then return January's payment as March's previous value.

The customer/month grid keeps February as a zero. March is consequently
classified as a return. The calendar must be consecutive and cover the
first subscription date; dbt tests these assumptions before building
downstream models.

## Retention and returns

The January cohort contains A, C and D. February retains A and D, giving
2/3. C returns in March, bringing it back to 3/3. This reports who is paying
in each observed month, rather than who has paid without interruption.

For NRR, a returning customer had no opening revenue and is excluded.
In February, existing customers retain $190 out of $270; the new $80
customer contributes to total MRR but not to that ratio.

## Source updates

The loader uses natural IDs and ON CONFLICT updates. A rerun replaces
prices and dates for those IDs and records another load. It leaves IDs
that are absent from the new batch in place.

That is enough for a fixed sample dataset. Importing a billing provider's
history would need an explicit policy for deletions and corrected periods.
