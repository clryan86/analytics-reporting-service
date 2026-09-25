from pathlib import Path
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

def test_api_kpis_snapshot_export(tmp_path: Path):
    client = TestClient(create_app(Settings(tmp_path / "a.db")))
    kpis = client.get("/api/kpis")
    assert kpis.status_code == 200
    assert kpis.json()["orders"] > 0
    snapshot = client.post("/api/snapshots", json={"report_name": "executive_summary", "parameters": {}})
    assert snapshot.status_code == 201
    assert client.get("/api/snapshots").json()[0]["report_name"] == "executive_summary"
    csv_export = client.get("/api/export/region.csv")
    assert csv_export.status_code == 200
    assert "dimension,orders,revenue" in csv_export.text
