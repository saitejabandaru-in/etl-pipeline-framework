import argparse
from pathlib import Path

from etl.config import load_config
from etl.metrics import PipelineMetrics
from etl.pipeline import ETLPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a configured ETL pipeline.")
    parser.add_argument("--config", default="pipeline_config.yaml", help="Path to pipeline YAML config.")
    parser.add_argument("--schedule", default="manual", help="Schedule label for orchestration logs.")
    args = parser.parse_args()

    config_path = Path(args.config)
    metrics = PipelineMetrics()
    pipeline = ETLPipeline(load_config(config_path), root=config_path.parent)

    try:
        result = pipeline.run()
        metrics.records_in = pipeline.lineage.events[0].rows
        metrics.records_out = len(result)
    except Exception as exc:
        metrics.errors.append(str(exc))
        raise
    finally:
        metrics.finish()

    print(f"pipeline={pipeline.config['name']} schedule={args.schedule}")
    print(f"records_in={metrics.records_in} records_out={metrics.records_out}")
    print(f"latency_seconds={metrics.latency_seconds:.4f} throughput={metrics.throughput:.2f}/s")
    print(pipeline.lineage.to_text())


if __name__ == "__main__":
    main()
