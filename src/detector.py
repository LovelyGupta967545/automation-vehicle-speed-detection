#Stage 1 (Detection): Detect vehicles in the video frames using YOLOv8 model
from ultralytics import YOLO
import supervision as sv # this librery use for simple and clean formet mai lane ke liye kyuki yolo ka jo output hota hai vo complex hota hai
from config import settings #ye settings.py file se import karega jisme video path, model path, thresholds, calibration points define hai
class Detector:
    def __init__(self):
      self.model = YOLO(settings.MODEL_PATH) #ye fun tabhi chlega jb detector class ka object banega
    def detect(self, frame):
        results=self.model( frame,conf=settings.CONFIDENCE_THRESHOLD,iou=settings.IOU_THRESHOLD,classes=settings.VEHICLE_CLASS_IDS, verbose=False,)[0]#isse terminal mein bar-bar detection ka detail print nahi hoga)
        detections = sv.Detections.from_ultralytics(results)
        return detections
""" note : flow hai is file ka →
Frame aata hai → Detector.detect(frame) call hota hai → 
YOLO model chalti hai us frame par (with confidence/iou/classes filter) → 
Result ko sv.Detections mein convert karke wapas bhejte hain""" 