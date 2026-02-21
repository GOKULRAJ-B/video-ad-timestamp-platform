import subprocess
import sys
from pathlib import Path


def extract_audio(video_path: str):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Automatically determine audio output path
    audio_dir = Path("data/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)

    audio_output_path = audio_dir / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        str(audio_output_path),
    ]

    subprocess.run(command, check=True)

    print(f"Audio extracted to {audio_output_path}")

    return audio_output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_audio_from_video.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    extract_audio(video_path)