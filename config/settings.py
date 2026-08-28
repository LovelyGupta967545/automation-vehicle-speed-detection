#video path, model, calibration points, thresholds all things define here
import numpy as np
VIDEO_SOURCE = "sample_data/traffic.mp4" # yha vedio inpu lenge
MODEL_PATH = "modules/yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.1      # 10% se kam confident detections ignore honge it means jinke rectangle hlka hoga vo ht jayega
IOU_THRESHOLD = 0.5   #50%+ overlap wale duplicate boxes ko NMS hata dega
VEHICLE_CLASS_IDS = [2, 3, 5, 7]   # car, motorcycle, bus, truck ki id define kre pecocdata set se
CLASS_NAME_MAP = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
# Apni video ke ek frame mein road ke 4 corners (pixels mein):
SOURCE = np.array([
    [960, 40], #top left corner
    [1180, 40], #top right corner
    [1880, 700], #bottom right corner
    [830, 700], #bottom left corner
])
TARGET_WIDTH = 11*10 # meters mai us road ki width kitni hai
TARGET_HEIGHT = 65*10 # meters mai us road ki height kitni hai
TARGET = np.array([
    [0, 0],
    [TARGET_WIDTH - 1, 0],
    [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
    [0, TARGET_HEIGHT - 1],
])#ye define karega ki road ke 4 corners ko target image ke 4 corners pe map karna hai
LINE_START = (830, 480) # counting line ka start point - original video frame ke pixels mein
LINE_END = (1880,400) # counting line ka end point - original video frame ke pixels mein
SPEED_LIMIT = 60 # speed limit in km/h
SPEED_SMOOTHING_WINDOW = 15 # ek gaadi ke 15 position-samples se speed average nikalna (stable reading ke liye)
FLASK_HOST = "0.0.0.0" # Flask server ka host
FLASK_PORT = 5000 # Flask server ka port
JPEG_QUALITY = 80 # JPEG image quality for streaming