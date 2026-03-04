import subprocess
import sys
from pathlib import Path


def run_step(command, description):
    print(f"\n--- {description} ---")
    subprocess.run(command, check=True)


def run_pipeline(video_path: str):

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    video_name = video_path.stem
    audio_path = f"data/audio/{video_name}.wav"

    # Step 1 — Extract audio
    run_step(
        ["python", "processing/extract_audio_from_video.py", str(video_path)],
        "Extracting audio from video",
    )

    # Step 2 — Audio features
    run_step(
        [
            "python",
            "processing/audio/extract_audio_features.py",
            audio_path,
            "output/audio/",
        ],
        "Extracting audio features",
    )

    # Step 3 — Video features
    run_step(
        [
            "python",
            "processing/video/extract_video_features.py",
            str(video_path),
            "output/video/",
        ],
        "Extracting video features",
    )

    # Step 4 — Merge features
    run_step(
        [
            "python",
            "processing/merge_audio_video_features.py",
            "output/audio/audio_features.parquet",
            "output/video/video_features.parquet",
            "output/merged/",
        ],
        "Merging audio and video features",
    )

    # Step 5 — Score ad timestamps
    run_step(
        [
            "python",
            "processing/score_ad_timestamps.py",
            "output/merged/merged_features.parquet",
            "output/gold/",
        ],
        "Scoring ad timestamps",
    )

    # Step 6 — Save to database
    run_step(
        [
            "python",
            "warehouse/save_to_db.py",
            "output/gold/ad_timestamps.parquet",
            str(video_path),
        ],
        "Saving results to database",
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    run_pipeline(video_path)