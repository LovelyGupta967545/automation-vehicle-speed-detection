# ye bs file help ke liye bnaye jo video frame bnaye hai vo web page pe dikhane chahte bs ye use jpg mtlb image form mai convert kr config setting.py se id leke jese 2 id hai to car show hogi
import cv2
from config import settings
def encode_jpeg(frame):
    ok, buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), settings.JPEG_QUALITY]
    )
    if not ok:
        raise RuntimeError("Failledyha frame encode nhi ho paya jpg form mai")
    return buffer.tobytes()
def class_name(class_id):
    return settings.CLASS_NAME_MAP.get(int(class_id), "vehicle")