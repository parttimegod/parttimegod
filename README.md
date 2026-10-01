## Emirhan Bahçacı

Based in Antalya, Türkiye, with a background in econometrics. I work as a
court clerk and build Python and SQL tools for data analysis and document
processing.

### [evds-mcp](https://github.com/parttimegod/evds-mcp)

An MCP server for the Central Bank of Türkiye's statistical database.
It finds series codes, retrieves observations and checks stationarity
before comparing time series.

The optional PostgreSQL store keeps observation values and fetch records
together. Its tests cover repeated imports, missing periods and rollback
when part of a batch fails.

### [saas-revenue-warehouse](projects/saas-revenue-warehouse)

Subscription revenue analysis in PostgreSQL and dbt. It separates new
customers, returns, upgrades, downgrades and cancellations, then builds
monthly revenue and cohort reports.

The sample data includes a customer with two subscriptions and another
who cancels and returns. Those cases matter: counting subscriptions as
customers inflates retention, and treating a return as acquisition
inflates new revenue. The larger demo uses generated data.

### [kvkk-maskeleme](https://github.com/parttimegod/kvkk-maskeleme)

Masks identifiers in Turkish documents using check-digit validation and
an optional local model for names and addresses. Replacement maps stay
local, and the output is checked again for remaining identifiers.

The README includes the evaluation dataset and its limitations.

Open to remote data, analytics engineering and Python backend roles.
