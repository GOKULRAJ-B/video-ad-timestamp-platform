import cv2
import pandas as pd
import sys
from pathlib import Path


def extract_video_features(video_path: str, output_dir: str):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_gray = None
    frame_idx = 0

    records = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            motion_intensity = diff.mean()

            timestamp = frame_idx / fps

            scene_change = motion_intensity > 20  # simple threshold

            records.append({
                "timestamp_sec": round(timestamp, 2),
                "motion_intensity": round(float(motion_intensity), 2),
                "scene_change": bool(scene_change)
            })

        prev_gray = gray
        frame_idx += 1

    cap.release()

    df = pd.DataFrame(records)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "video_features.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Video features saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_video_features.py <video_path> <output_dir>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2]

    extract_video_features(video_path, output_dir)
