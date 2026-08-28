"""
Stage 2: ByteTrack tracking + LineZone counting + Speed calculation + annotations
"""
import supervision as sv
from config import settings
from src.detector import Detector
from src.speed_estimator import SpeedEstimator
from collections import defaultdict
class VehicleAnalyzer:
    def __init__(self):
        self.detector = Detector()
        self.tracker = sv.ByteTrack()
        self.speed_estimator = SpeedEstimator()
        self.violations = []
        self.vehicle_type_counts = defaultdict(int)
        self.line_zone = sv.LineZone(start=sv.Point(*settings.LINE_START), end=sv.Point(*settings.LINE_END))
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.line_annotator = sv.LineZoneAnnotator()

    def process_frame(self, frame, video_time):
        detections = self.detector.detect(frame)
        detections = self.tracker.update_with_detections(detections)
        # Speed calculate karo — har vehicle ka bottom-center point nikalo
        points = detections.get_anchors_coordinates(anchor=sv.Position.BOTTOM_CENTER)
        speeds = {}
        if detections.tracker_id is not None and len(detections.tracker_id) > 0:
            speeds = self.speed_estimator.update(detections.tracker_id, points, video_time)
        # Har vehicle ke liye custom label banao (ID + type + speed) + violation check
        labels = []
        if detections.tracker_id is not None and len(detections.tracker_id) > 0:
            for tracker_id, class_id in zip(detections.tracker_id, detections.class_id):
                vehicle_type = settings.CLASS_NAME_MAP.get(int(class_id), "vehicle")
                speed_kmh = speeds.get(tracker_id)
                speed_text = f"{speed_kmh:.1f}km/h" if speed_kmh is not None else "..."
                labels.append(f"#{tracker_id} {vehicle_type} {speed_text}")

                if speed_kmh is not None and speed_kmh > settings.SPEED_LIMIT:
                    self.violations.append({
                        "tracker_id": int(tracker_id),
                        "vehicle_type": vehicle_type,
                        "speed": round(speed_kmh, 1),
                    })
        # Counting (line crossing)
        crossed_in, crossed_out = self.line_zone.trigger(detections)
        for is_in, class_id in zip(crossed_in, detections.class_id):
            if is_in:
                vehicle_type = settings.CLASS_NAME_MAP.get(int(class_id), "vehicle")
                self.vehicle_type_counts[vehicle_type] += 1
        annotated_frame = frame.copy()
        annotated_frame = self.box_annotator.annotate(annotated_frame, detections)
        annotated_frame = self.label_annotator.annotate(annotated_frame, detections, labels=labels)
        annotated_frame = self.line_annotator.annotate(annotated_frame, self.line_zone)
        stats = {
            "in_count": self.line_zone.in_count,
            "out_count": self.line_zone.out_count,
            "vehicle_type_counts": dict(self.vehicle_type_counts),
            "violations": self.violations[-20:],
        }
        return annotated_frame, stats