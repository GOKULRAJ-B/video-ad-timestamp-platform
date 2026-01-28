import pandas as pd
import sys
from pathlib import Path


def score_ad_slots(merged_path: str, output_dir: str):
    df = pd.read_parquet(merged_path)

    # Sort by time
    df = df.sort_values("timestamp_sec")

    ad_slots = []
    window_start = None
    scores = []

    for _, row in df.iterrows():
        good_window = (
            row["is_silence"]
            and not row["scene_change"]
            and row["motion_intensity"] < 15
        )

        if good_window:
            if window_start is None:
                window_start = row["timestamp_sec"]
            scores.append(
                1.0
                - (row["motion_intensity"] / 50)
            )
        else:
            if window_start is not None and len(scores) >= 2:
                ad_slots.append({
                    "ad_start_sec": window_start,
                    "ad_end_sec": row["timestamp_sec"],
                    "confidence_score": round(sum(scores) / len(scores), 2),
                    "reason": "silence + stable scene"
                })
            window_start = None
            scores = []

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "ad_timestamps.parquet"
    pd.DataFrame(ad_slots).to_parquet(output_path, index=False)

    print(f"Ad timestamps saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python score_ad_timestamps.py "
            "<merged_features.parquet> <output_dir>"
        )
        sys.exit(1)

    merged_path = sys.argv[1]
    output_dir = sys.argv[2]

    score_ad_slots(merged_path, output_dir)
