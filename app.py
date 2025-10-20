from flask import Flask, send_file

from picamera_wrapper import PicameraWrapper


picam = PicameraWrapper()
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


@app.route("/")
def home():
    return send_file("index.html")
