from pathlib import Path

from analytics.kpis import group, report, summary
from analytics.store import AnalyticsStore

def test_seed_and_kpis(tmp_path: Path):
    store = AnalyticsStore(tmp_path / "a.db")
    store.seed(10)
    kpis = summary(store)
    assert kpis["orders"] > 0
    assert kpis["revenue"] > kpis["gross_profit"] > 0
    assert 0 < kpis["gross_margin_percent"] < 100
    assert len(group(store, "region")) == 4

def test_report_shapes(tmp_path: Path):
    store = AnalyticsStore(tmp_path / "a.db")
    store.seed(7)
    result = report(store, "executive_summary", {})
    assert "summary" in result
    assert len(result["by_channel"]) == 3
