"""Airflow DAG definition for scheduled ETL execution.

Airflow is optional for local development. If installed, this module exposes
`etl_pipeline_dag`; otherwise it can still be imported by tests and linters.
"""

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
except ModuleNotFoundError:
    DAG = None
    BashOperator = None


if DAG and BashOperator:
    from datetime import datetime

    with DAG(
        dag_id="etl_pipeline_framework",
        start_date=datetime(2026, 1, 1),
        schedule="@hourly",
        catchup=False,
        tags=["etl", "data-engineering"],
    ) as etl_pipeline_dag:
        run_pipeline = BashOperator(
            task_id="run_pipeline",
            bash_command="python -m etl.run --config pipeline_config.yaml --schedule hourly",
        )
else:
    etl_pipeline_dag = None
