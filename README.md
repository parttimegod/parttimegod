## Emirhan Bahçacı

Econometrics student in Antalya, Türkiye, working as a court clerk at the
Ministry of Justice. I write Python tools for problems where being
confidently wrong is worse than returning nothing.

Both projects below are built on one idea: don't warn about the wrong
answer, make it unreachable.

---

### [kvkk-maskeleme](https://github.com/parttimegod/kvkk-maskeleme)

Detects and masks personal data in Turkish text, so a document can be
processed — or sent to a cloud model — without its identifiers leaving
the building.

Check-digit validation for the identifiers that have one. A locally run
model for names and addresses, which no pattern can find. Masked output
is re-scanned, and a surviving identifier raises an exception rather
than ship a leak quietly.

Measured over 220 generated documents: 100% on every pattern-matched
type, 99.5% on names, 0 false positives on 30 control sentences built
around near-miss traps.

Every one of those numbers started out worse. Making the test harder is
what found the real problems — names written without a label, addresses
that were being masked only halfway, and a model configuration that
silently returned nothing at all.

---

### [evds-mcp](https://github.com/parttimegod/evds-mcp)

An MCP server over the Central Bank of Türkiye's statistical database,
so a model can pull Turkish macroeconomic data and analyse it without
inventing series codes.

It has no raw correlation tool, deliberately. USD/TRY against CPI
correlates at 0.99 in levels and 0.57 log-differenced at a one-month
lag. The first figure is spurious, the lag is not contemporaneous, and
a tool that hands over the first number without saying so is worse than
no tool.

---

Open to remote backend and data engineering work.
