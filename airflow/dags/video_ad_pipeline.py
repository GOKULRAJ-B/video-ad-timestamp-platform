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

    extract_audio = BashOperator(
        task_id="extract_audio_features",
        bash_command=(
            "python processing/audio/extract_audio_features.py "
            "data/audio/sample.wav output/audio/"
        ),
        cwd=BASE_PATH,
    )

    extract_video = BashOperator(
        task_id="extract_video_features",
        bash_command=(
            "python processing/video/extract_video_features.py "
            "data/video/sample.mp4 output/video/"
        ),
        cwd=BASE_PATH,
    )

    merge_features = BashOperator(
        task_id="merge_audio_video_features",
        bash_command=(
            "python processing/merge_audio_video_features.py "
            "output/audio/audio_features.parquet "
            "output/video/video_features.parquet "
            "output/merged/"
        ),
        cwd=BASE_PATH,
    )

    score_ads = BashOperator(
        task_id="score_ad_timestamps",
        bash_command=(
            "python processing/score_ad_timestamps.py "
            "output/merged/merged_features.parquet "
            "output/gold/"
        ),
        cwd=BASE_PATH,
    )

    [extract_audio, extract_video] >> merge_features >> score_ads
