import pandas as pd


def clean(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    cleaned = frame.copy()
    if config.get("drop_duplicates", False):
        cleaned = cleaned.drop_duplicates()
    for column, value in config.get("fill_missing", {}).items():
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna(value)
    return cleaned
