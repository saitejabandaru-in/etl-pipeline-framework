from pathlib import Path

import pandas as pd


class LakeLoader:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self, frame: pd.DataFrame) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.suffix.lower() == ".parquet":
            frame.to_parquet(self.path, index=False)
        else:
            frame.to_csv(self.path, index=False)
