import pandas as pd
import sqlite3
import sys
from pathlib import Path


def save_to_database(parquet_path: str, video_path: str):

    df = pd.read_parquet(parquet_path)

    video_name = Path(video_path).stem
    db_path = "warehouse/ad_slots.db"

    conn = sqlite3.connect(db_path)

    df.to_sql(video_name, conn, if_exists="replace", index=False)

    conn.close()

    print(f"Saved ad slots to table '{video_name}' in {db_path}")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python save_to_db.py <ad_timestamps.parquet> <video_path>")
        sys.exit(1)

    parquet_path = sys.argv[1]
    video_path = sys.argv[2]

    save_to_database(parquet_path, video_path)