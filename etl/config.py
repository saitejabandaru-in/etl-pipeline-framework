from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    """Load a pipeline YAML config."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
