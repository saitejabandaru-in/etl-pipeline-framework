from pathlib import Path

import pandas as pd


class CSVExtractor:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def extract(self) -> pd.DataFrame:
        if not self.path.exists():
            raise FileNotFoundError(f"CSV source not found: {self.path}")
        return pd.read_csv(self.path)
