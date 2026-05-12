import pandas as pd


def normalize(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    normalized = frame.copy()
    for column, operation in config.get("columns", {}).items():
        if column not in normalized.columns:
            continue
        series = normalized[column].astype(str).str.strip()
        if operation == "lower":
            normalized[column] = series.str.lower()
        elif operation == "upper":
            normalized[column] = series.str.upper()
        elif operation == "title":
            normalized[column] = series.str.title()
        else:
            raise ValueError(f"Unsupported normalization operation: {operation}")
    return normalized
