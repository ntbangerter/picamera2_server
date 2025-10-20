from flask import Flask, send_file
from io import BytesIO
from picamera2 import Picamera2
import numpy as np


picam = Picamera2()
picam.start()

app = Flask(__name__)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/capture_jpeg")
def capture_jpeg():
    buf = BytesIO()
    picam.capture_file(buf, format="jpeg")
    buf.seek(0)
    
    return send_file(buf, mimetype='image/jpeg')


@app.route("/capture_array")
def capture_array():
    img_array = picam.capture_array()
    buf = BytesIO()
    np.save(buf, img_array)
    buf.seek(0)

    return send_file(buf, mimetype='application/octet-stream')


@app.route("/")
def home():
    return send_file("index.html")
