from __future__ import annotations
import json
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SCHEMA = """CREATE TABLE IF NOT EXISTS sales(
 id INTEGER PRIMARY KEY AUTOINCREMENT,order_date TEXT NOT NULL,region TEXT NOT NULL,channel TEXT NOT NULL,
 customer_id TEXT NOT NULL,revenue REAL NOT NULL,cost REAL NOT NULL,units INTEGER NOT NULL);
 CREATE TABLE IF NOT EXISTS report_snapshots(
 id INTEGER PRIMARY KEY AUTOINCREMENT,report_name TEXT NOT NULL,parameters_json TEXT NOT NULL,
 result_json TEXT NOT NULL,created_at TEXT NOT NULL);"""

class AnalyticsStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def conn(self):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        try:
            yield c
            c.commit()
        finally:
            c.close()

    def seed(self, days=120):
        with self.conn() as c:
            if c.execute("select count(*) from sales").fetchone()[0]:
                return
            start = date(2026, 5, 1)
            regions = ["Northeast", "South", "Midwest", "West"]
            channels = ["Web", "Partner", "Direct"]
            customer_id = 1000
            for d in range(days):
                day = start + timedelta(days=d)
                for r_i, region in enumerate(regions):
                    for ch_i, channel in enumerate(channels):
                        orders = 2 + ((d + r_i + ch_i) % 5)
                        for j in range(orders):
                            revenue = round(80 + (d % 17) * 7 + r_i * 18 + ch_i * 25 + j * 12.5, 2)
                            margin = .28 + ((r_i + ch_i) % 3) * .05
                            cost = round(revenue * (1 - margin), 2)
                            units = 1 + ((d + j + ch_i) % 6)
                            customer_id += 1
                            c.execute(
                                "INSERT INTO sales(order_date,region,channel,customer_id,revenue,cost,units) VALUES(?,?,?,?,?,?,?)",
                                (day.isoformat(), region, channel, f"C{customer_id % 180:04d}", revenue, cost, units),
                            )

    def query(self, sql, params=()):
        with self.conn() as c:
            return [dict(r) for r in c.execute(sql, params).fetchall()]

    def snapshot(self, name, params, result):
        with self.conn() as c:
            cur = c.execute(
                "INSERT INTO report_snapshots(report_name,parameters_json,result_json,created_at) VALUES(?,?,?,?)",
                (name, json.dumps(params), json.dumps(result), datetime.now(timezone.utc).isoformat()),
            )
            return int(cur.lastrowid)

    def snapshots(self, limit=30):
        with self.conn() as c:
            rows = c.execute("select * from report_snapshots order by id desc limit ?", (limit,)).fetchall()
        return [{**dict(r), "parameters": json.loads(r["parameters_json"]), "result": json.loads(r["result_json"])} for r in rows]
