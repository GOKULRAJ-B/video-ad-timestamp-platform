from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

BASE_PATH = "/opt/project"

default_args = {
    "owner": "data-platform",
    "retries": 2,
}

with DAG(
    dag_id="video_ad_timestamp_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["video", "ads", "data-engineering"],
) as dag:

    run_video_pipeline = BashOperator(
        task_id="run_video_ad_pipeline",
        bash_command=(
            "python scripts/run_pipeline.py data/raw/sample1.mp4"
        ),
        cwd=BASE_PATH,
    )

    run_video_pipeline