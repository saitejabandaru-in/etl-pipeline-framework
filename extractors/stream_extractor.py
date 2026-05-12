import pandas as pd


class StreamExtractor:
    def __init__(self, messages: list[dict]) -> None:
        self.messages = messages

    def extract(self) -> pd.DataFrame:
        return pd.DataFrame(self.messages)
