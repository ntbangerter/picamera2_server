from flask import Flask, Response, send_file

from picamera import Picamera


picam = Picamera()
app = Flask(__name__)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/capture_jpeg")
def capture_jpeg():
    return send_file(
        picam.capture_jpeg(),
        mimetype='image/jpeg'
    )


@app.route("/capture_array")
def capture_array():
    return send_file(
        picam.capture_array(),
        mimetype='application/octet-stream',
    )


@app.route('/video_feed')
def video_feed():
    """Route that returns the MJPEG stream."""
    return Response(
        picam.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame',
        direct_passthrough=True,
    )


@app.route("/")
def home():
    return send_file("index.html")


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        picam2.stop_recording()
