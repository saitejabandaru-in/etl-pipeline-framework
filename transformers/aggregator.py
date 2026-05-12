import pandas as pd


def aggregate(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    group_by = config["group_by"]
    metrics = config["metrics"]
    aggregated = frame.groupby(group_by, as_index=False).agg(metrics)
    aggregated.columns = [
        "_".join(column).strip("_") if isinstance(column, tuple) else column for column in aggregated.columns
    ]
    return aggregated
