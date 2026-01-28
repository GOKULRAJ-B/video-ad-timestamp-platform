import pandas as pd
import sys
from pathlib import Path


def merge_features(audio_path: str, video_path: str, output_dir: str):
    audio_df = pd.read_parquet(audio_path)
    video_df = pd.read_parquet(video_path)

    # ---- Downsample video to 1-second resolution ----
    video_df["timestamp_sec"] = video_df["timestamp_sec"].round(0)

    video_agg = (
        video_df.groupby("timestamp_sec")
        .agg({
            "motion_intensity": "mean",
            "scene_change": "max"
        })
        .reset_index()
    )

    # ---- Round audio timestamps for alignment ----
    audio_df["timestamp_sec"] = audio_df["timestamp_sec"].round(0)

    # ---- Merge on timestamp ----
    merged_df = pd.merge(
        audio_df,
        video_agg,
        on="timestamp_sec",
        how="inner"
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "merged_features.parquet"
    merged_df.to_parquet(output_path, index=False)

    print(f"Merged features saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python merge_audio_video_features.py "
            "<audio_features.parquet> <video_features.parquet> <output_dir>"
        )
        sys.exit(1)

    audio_path = sys.argv[1]
    video_path = sys.argv[2]
    output_dir = sys.argv[3]

    merge_features(audio_path, video_path, output_dir)
