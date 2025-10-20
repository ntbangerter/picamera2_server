from io import BytesIO
from picamera2 import Picamera2
import numpy as np


class PicameraWrapper:

    def __init__(self):
        self.picam = Picamera2()
        self.picam.start()

    def capture_jpeg(self):
        buf = BytesIO()
        self.picam.capture_file(buf, format="jpeg")
        buf.seek(0)
        return buf

    def capture_array(self):
        img_array = self.picam.capture_array()
        buf = BytesIO()
        np.save(buf, img_array)
        buf.seek(0)
        return buf
