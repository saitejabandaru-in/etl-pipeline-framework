from collections.abc import Mapping

import pandas as pd
import requests


class APIExtractor:
    def __init__(self, url: str, params: Mapping[str, str] | None = None, records_path: str | None = None) -> None:
        self.url = url
        self.params = params
        self.records_path = records_path

    def extract(self) -> pd.DataFrame:
        response = requests.get(self.url, params=self.params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if self.records_path:
            for key in self.records_path.split("."):
                payload = payload[key]
        return pd.DataFrame(payload)
