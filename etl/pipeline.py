from pathlib import Path

import pandas as pd

from extractors.api_extractor import APIExtractor
from extractors.csv_extractor import CSVExtractor
from extractors.db_extractor import DBExtractor
from extractors.stream_extractor import StreamExtractor
from loaders.lake_loader import LakeLoader
from loaders.warehouse_loader import WarehouseLoader
from quality.checks import run_quality_checks
from quality.lineage import LineageTracker
from transformers.aggregator import aggregate
from transformers.cleaner import clean
from transformers.normalizer import normalize


class ETLPipeline:
    """Config-driven extract-transform-load pipeline."""

    def __init__(self, config: dict, root: str | Path = ".") -> None:
        self.config = config["pipeline"]
        self.root = Path(root)
        self.lineage = LineageTracker(self.config["name"])

    def run(self) -> pd.DataFrame:
        frame = self._extract()
        self.lineage.record("extract", rows=len(frame), details=self.config["source"])

        for transform in self.config.get("transforms", []):
            frame = self._transform(frame, transform)
            self.lineage.record(f"transform:{transform['type']}", rows=len(frame), details=transform)

        quality_result = run_quality_checks(frame, self.config.get("quality", {}))
        self.lineage.record("quality", rows=len(frame), details=quality_result.as_dict())
        if not quality_result.passed:
            raise ValueError(f"Data quality failed: {quality_result.failures}")

        self._load(frame)
        self.lineage.record("load", rows=len(frame), details=self.config["target"])
        return frame

    def _extract(self) -> pd.DataFrame:
        source = self.config["source"]
        source_type = source["type"]
        if source_type == "csv":
            return CSVExtractor(self.root / source["path"]).extract()
        if source_type == "api":
            return APIExtractor(source["url"], source.get("params"), source.get("records_path")).extract()
        if source_type == "db":
            return DBExtractor(source["connection_url"], source["query"]).extract()
        if source_type == "stream":
            return StreamExtractor(source["messages"]).extract()
        raise ValueError(f"Unsupported source type: {source_type}")

    def _transform(self, frame: pd.DataFrame, transform: dict) -> pd.DataFrame:
        transform_type = transform["type"]
        if transform_type == "clean":
            return clean(frame, transform)
        if transform_type == "normalize":
            return normalize(frame, transform)
        if transform_type == "aggregate":
            return aggregate(frame, transform)
        raise ValueError(f"Unsupported transform type: {transform_type}")

    def _load(self, frame: pd.DataFrame) -> None:
        target = self.config["target"]
        target_type = target["type"]
        if target_type == "lake":
            LakeLoader(self.root / target["path"]).load(frame)
            return
        if target_type == "warehouse":
            WarehouseLoader(target["connection_url"], target["table"]).load(frame)
            return
        raise ValueError(f"Unsupported target type: {target_type}")
