# Interview Guide

## 30-second explanation

> Analytics Reporting Service is a SQL-backed metrics layer. I centralized KPI definitions such as revenue, gross profit, margin, customers and average order value, then exposed them through filtered APIs, reusable report compositions, saved snapshots, CSV exports and a dashboard.

## Why snapshots?

A report snapshot preserves the exact parameters and result at a point in time. That is useful for auditability and avoids confusion when underlying data changes after a report is distributed.

## Why put metrics behind an API?

It creates one source of truth for definitions and lets BI tools, dashboards, scheduled jobs or applications consume identical business logic.

## Resume bullets

- Built a SQL-backed analytics service centralizing KPI definitions, date/segment filtering, report composition and CSV exports.
- Added persisted report snapshots for auditability and reproducibility plus deterministic seeded warehouse data.
- Delivered FastAPI endpoints, executive dashboard, automated tests, Docker and CI.
