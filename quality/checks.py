from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    failures: list[str]

    def as_dict(self) -> dict:
        return {"passed": self.passed, "failures": self.failures}


def run_quality_checks(frame: pd.DataFrame, rules: dict) -> QualityResult:
    failures: list[str] = []

    required_columns = set(rules.get("required_columns", []))
    missing_columns = required_columns.difference(frame.columns)
    if missing_columns:
        failures.append(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    for column in rules.get("non_null", []):
        if column in frame.columns and frame[column].isna().any():
            failures.append(f"Column has null values: {column}")

    for column in rules.get("unique", []):
        if column in frame.columns and frame[column].duplicated().any():
            failures.append(f"Column has duplicate values: {column}")

    for column, minimum in rules.get("min_values", {}).items():
        if column in frame.columns and (frame[column] < minimum).any():
            failures.append(f"Column contains values below {minimum}: {column}")

    return QualityResult(passed=not failures, failures=failures)
