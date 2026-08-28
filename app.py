import threading
import cv2
from flask import Flask, Response, jsonify, render_template
from config import settings
from src import VehicleAnalyzer, encode_jpeg
app = Flask(__name__)
analyzer = VehicleAnalyzer()
latest_stats = {
    "in_count": 0,
    "out_count": 0,
    "vehicle_type_counts": {},
    "violations": [],
}
stats_lock = threading.Lock()
def generate_frames():
    cap = cv2.VideoCapture(settings.VIDEO_SOURCE)
    if not cap.isOpened():
        raise RuntimeError(f"Video open nahi hui: {settings.VIDEO_SOURCE}")
    while True:
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
            continue
        video_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0   
        annotated, stats = analyzer.process_frame(frame, video_time)  
       
        with stats_lock:
            latest_stats.update(stats)
            jpeg_bytes = encode_jpeg(annotated)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n"
        )
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )
@app.route("/stats")
def stats():
    with stats_lock:
        return jsonify(latest_stats)
    
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/analytics")
def analytics():
    with stats_lock:
        return render_template("analytics.html", stats=latest_stats)
@app.route("/reports")
def reports():
    with stats_lock:
        return render_template("reports.html", stats=latest_stats)
    
@app.route("/settings-ui")
def settings_ui():
    return render_template("settings_ui.html", settings=settings)
if __name__ == "__main__":
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, threaded=True, debug=False)


            


