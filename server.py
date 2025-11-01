from flask import Flask, Response, send_file, request

from picamera import Picamera


picam = Picamera()
app = Flask(__name__)
TRUTHY = ('true', '1', 'yes')


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/capture_jpeg")
def capture_jpeg():
    # read optional ?high_res= flag (default=true)
    high_res = request.args.get('high_res', 'true').lower() in TRUTHY
    return send_file(
        picam.capture_jpeg(high_res=high_res),
        mimetype='image/jpeg'
    )


@app.route("/capture_array")
def capture_array():
    # read optional ?high_res= flag (default=true)
    high_res = request.args.get('high_res', 'true').lower() in TRUTHY
    return send_file(
        picam.capture_array(high_res=high_res),
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
        app.run(
            host='0.0.0.0',
            port=8000,
            threaded=True,
        )
    finally:
        picam.stop_recording()
