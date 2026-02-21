# import pandas as pd

# df = pd.read_parquet("output/gold/ad_timestamps.parquet")

# print(df.head())
# print("\nTotal Ad Slots:", len(df))

# import cv2

# cap = cv2.VideoCapture("data/video/sample.mp4")
# fps = cap.get(cv2.CAP_PROP_FPS)
# frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# duration = frames / fps
# print("Video Duration (sec):", duration)


import pandas as pd

df = pd.read_parquet("output/gold/ad_timestamps.parquet")
print((df["ad_end_sec"] > df["ad_start_sec"]).all())