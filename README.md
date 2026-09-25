# Analytics Reporting Service

[![CI](https://github.com/clryan86/analytics-reporting-service/actions/workflows/ci.yml/badge.svg)](https://github.com/clryan86/analytics-reporting-service/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![SQL](https://img.shields.io/badge/SQL-KPI%20engine-4479A1)
![FastAPI](https://img.shields.io/badge/FastAPI-reporting-009688)

A backend analytics service that centralizes **KPI definitions, date/segment filters, reusable reports, saved snapshots, CSV exports, and an executive dashboard** over a reproducible sales dataset.

## Why this project matters

Analytics teams often end up with different definitions of revenue, margin, orders, or customer counts across dashboards and spreadsheets. This service puts metric logic behind a single API and SQL layer so consumers share the same definitions.

## KPIs

- revenue
- cost
- gross profit
- gross margin %
- orders
- average order value
- units
- distinct customers

Filters support date range, region and channel. Breakdowns are available by region, channel and day.

## Built-in reports

- `executive_summary`
- `daily_trend`

Reports can be saved as immutable snapshots for audit/reproducibility, and grouped outputs can be exported as CSV.

## Quick start

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The demo data seeds automatically. Open `/` for the dashboard and `/docs` for OpenAPI.

## Engineering features

- centralized SQL metric definitions
- parameterized filtering
- reusable report composition
- deterministic sample data
- persisted report snapshots
- CSV streaming exports
- typed FastAPI service
- automated tests
- Docker and GitHub Actions

## Roadmap

- semantic metric registry
- scheduled report delivery
- Power BI/Fabric-ready endpoints
- row-level security
- PostgreSQL warehouse profile
- PDF/XLSX exports
- report subscriptions
- metric freshness indicators
- cached aggregates

## Author

**Christopher Ryan**  
Python • SQL • Analytics • Data Automation

## License

MIT
