from __future__ import annotations
from .store import AnalyticsStore

def where(start=None, end=None, region=None, channel=None):
    clauses = []
    params = []
    for column, value, op in [
        ("order_date", start, ">="), ("order_date", end, "<="), ("region", region, "="), ("channel", channel, "=")
    ]:
        if value:
            clauses.append(f"{column} {op} ?")
            params.append(value)
    return (" WHERE " + " AND ".join(clauses) if clauses else ""), params

def summary(store: AnalyticsStore, start=None, end=None, region=None, channel=None):
    w, p = where(start, end, region, channel)
    row = store.query(
        f"""SELECT COUNT(*) orders,ROUND(COALESCE(SUM(revenue),0),2) revenue,
        ROUND(COALESCE(SUM(cost),0),2) cost,COALESCE(SUM(units),0) units,
        COUNT(DISTINCT customer_id) customers,ROUND(COALESCE(AVG(revenue),0),2) avg_order_value
        FROM sales{w}""", p
    )[0]
    row["gross_profit"] = round(row["revenue"] - row["cost"], 2)
    row["gross_margin_percent"] = round(row["gross_profit"] / row["revenue"] * 100, 2) if row["revenue"] else 0
    return row

def group(store, dimension, start=None, end=None):
    if dimension not in {"region", "channel", "order_date"}:
        raise ValueError("Unsupported dimension")
    w, p = where(start, end)
    return store.query(
        f"""SELECT {dimension} dimension,COUNT(*) orders,ROUND(SUM(revenue),2) revenue,
        ROUND(SUM(revenue-cost),2) gross_profit,SUM(units) units
        FROM sales{w} GROUP BY {dimension} ORDER BY revenue DESC""", p
    )

def report(store, name, params):
    if name == "executive_summary":
        return {
            "summary": summary(store, **params),
            "by_region": group(store, "region", params.get("start"), params.get("end")),
            "by_channel": group(store, "channel", params.get("start"), params.get("end")),
        }
    if name == "daily_trend":
        return {"rows": group(store, "order_date", params.get("start"), params.get("end"))}
    raise ValueError("Unknown report")
