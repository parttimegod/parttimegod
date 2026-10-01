CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.customer (
    customer_id bigint PRIMARY KEY,
    segment text NOT NULL CHECK (segment IN ('small_business', 'mid_market')),
    country text NOT NULL
);
CREATE TABLE IF NOT EXISTS raw.subscription_period (
    period_id text PRIMARY KEY,
    customer_id bigint NOT NULL REFERENCES raw.customer(customer_id),
    subscription_id text NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    monthly_price numeric(12,2) NOT NULL CHECK (monthly_price > 0),
    CHECK (valid_to IS NULL OR valid_from < valid_to)
);
CREATE INDEX IF NOT EXISTS period_customer_start
    ON raw.subscription_period (customer_id, valid_from);
CREATE TABLE IF NOT EXISTS raw.calendar (
    month date PRIMARY KEY CHECK (extract(day FROM month) = 1)
);
CREATE TABLE IF NOT EXISTS raw.load_run (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    source text NOT NULL,
    customer_count integer NOT NULL CHECK (customer_count >= 0),
    period_count integer NOT NULL CHECK (period_count >= 0)
);
