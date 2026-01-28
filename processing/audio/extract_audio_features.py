import librosa
import numpy as np
import pandas as pd
import sys
from pathlib import Path


def extract_audio_features(audio_path: str, output_dir: str):
    y, sr = librosa.load(audio_path, sr=None)

    # RMS energy
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(
        range(len(rms)), sr=sr, hop_length=512
    )

    # Silence detection (simple threshold-based)
    silence_threshold = np.percentile(rms, 20)
    silence_frames = rms < silence_threshold

    data = []
    for t, r, s in zip(rms_times, rms, silence_frames):
        data.append({
            "timestamp_sec": round(float(t), 2),
            "rms_energy": float(r),
            "is_silence": bool(s)
        })

    df = pd.DataFrame(data)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "audio_features.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Audio features saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_audio_features.py <audio_path> <output_dir>")
        sys.exit(1)

    audio_path = sys.argv[1]
    output_dir = sys.argv[2]

    extract_audio_features(audio_path, output_dir)
