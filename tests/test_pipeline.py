from pathlib import Path

from etl.config import load_config
from etl.pipeline import ETLPipeline
from quality.checks import run_quality_checks


ROOT = Path(__file__).resolve().parents[1]


def test_sample_pipeline_runs(tmp_path):
    config = load_config(ROOT / "pipeline_config.yaml")
    config["pipeline"]["target"]["path"] = str(tmp_path / "region_revenue.csv")

    result = ETLPipeline(config, root=ROOT).run()

    assert result["revenue"].sum() == 7586.5
    assert set(result["region"]) == {"Asia Pacific", "Europe", "North America"}
    assert (tmp_path / "region_revenue.csv").exists()


def test_quality_checks_report_failures():
    config = load_config(ROOT / "pipeline_config.yaml")
    rules = {"unique": ["order_id"]}
    frame = ETLPipeline(config, root=ROOT)._extract()
    frame.loc[0, "order_id"] = frame.loc[1, "order_id"]

    result = run_quality_checks(frame, rules)

    assert not result.passed
    assert "Column has duplicate values: order_id" in result.failures
