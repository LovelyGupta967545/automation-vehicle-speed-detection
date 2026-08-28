#Stage 2 yha ho rhi speed calculation: Perspective transform + speed calculation

"""Formula:
    1. Track bottom-center (x, y) of each vehicle          -> centroid
    2. d_pixel = euclidean distance between two samples     -> pixels
    3. d_real  = perspective_transform(d_pixel)               -> meters
    4. speed   = (d_real / delta_t) * 3.6                       -> km/h
"""
import cv2
import numpy as np
from collections import deque,defaultdict 
import time
from config import settings
class ViewTransformer:
     def __init__(self, source: np.ndarray, target: np.ndarray):
        source = source.astype(np.float32)
        target = target.astype(np.float32)
        self.m = cv2.getPerspectiveTransform(source, target)
     def transform_points(self, points: np.ndarray) -> np.ndarray:
        if points.size == 0:
            return points
        reshaped = points.reshape(-1, 1, 2).astype(np.float32)
        transformed = cv2.perspectiveTransform(reshaped, self.m)
        return transformed.reshape(-1, 2)
class SpeedEstimator:
    def __init__(self):
        self.view_transformer = ViewTransformer(settings.SOURCE, settings.TARGET)
        self.coordinates = defaultdict(lambda: deque(maxlen=settings.SPEED_SMOOTHING_WINDOW))
        self.speeds = {}
    def update(self, tracker_ids, pixel_points, video_time):
        real_points = self.view_transformer.transform_points(pixel_points)
        now = video_time
        for tracker_id, (rx, ry) in zip(tracker_ids, real_points):
            self.coordinates[tracker_id].append((now, (rx, ry)))
            speed = self._estimate_speed(tracker_id)
            if speed is not None:
                self.speeds[tracker_id] = speed
        return self.speeds
    def _estimate_speed(self, tracker_id):
        history = self.coordinates[tracker_id]
        if len(history) < 2:
            return None
        (t0, p0), (t1, p1) = history[0], history[-1]
        delta_t = t1 - t0
        if delta_t <= 0:
            return None
        d_real = float(np.linalg.norm(np.array(p1) - np.array(p0)))  # meters
        speed_mps = d_real / delta_t
        return speed_mps * 3.6
        

