from __future__ import annotations
import csv
import io
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from analytics.kpis import group, report, summary
from analytics.store import AnalyticsStore
from .config import Settings

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = Jinja2Templates(directory=str(ROOT / "templates"))

class SnapshotRequest(BaseModel):
    report_name: str
    parameters: dict = {}

def create_app(settings: Settings | None = None):
    settings = settings or Settings.from_env()
    store = AnalyticsStore(settings.database_path)
    store.seed()
    app = FastAPI(title=settings.app_name, version="1.0.0")
    app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

    @app.get("/healthz")
    def health():
        return {"ok": True}

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return TEMPLATES.TemplateResponse(
            request=request, name="index.html",
            context={"app_name": settings.app_name, "summary": summary(store), "regions": group(store, "region"),
                     "channels": group(store, "channel"), "snapshots": store.snapshots(8)}
        )

    @app.get("/api/kpis")
    def kpis(start: str | None = None, end: str | None = None, region: str | None = None, channel: str | None = None):
        return summary(store, start, end, region, channel)

    @app.get("/api/breakdown/{dimension}")
    def breakdown(dimension: str, start: str | None = None, end: str | None = None):
        try:
            return group(store, dimension, start, end)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get("/api/reports/{name}")
    def get_report(name: str, start: str | None = None, end: str | None = None):
        try:
            return report(store, name, {"start": start, "end": end})
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc

    @app.post("/api/snapshots", status_code=201)
    def snapshot(req: SnapshotRequest):
        try:
            result = report(store, req.report_name, req.parameters)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc
        sid = store.snapshot(req.report_name, req.parameters, result)
        return {"snapshot_id": sid, "report_name": req.report_name, "result": result}

    @app.get("/api/snapshots")
    def snapshots():
        return store.snapshots()

    @app.get("/api/export/{dimension}.csv")
    def export(dimension: str):
        try:
            rows = group(store, dimension)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["dimension", "orders", "revenue", "gross_profit", "units"])
        writer.writeheader()
        writer.writerows(rows)
        return StreamingResponse(
            iter([output.getvalue()]), media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={dimension}-report.csv"},
        )

    return app

app = create_app()
