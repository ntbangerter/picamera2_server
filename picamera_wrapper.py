from io import BytesIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import numpy as np


class PicameraWrapper:

    def __init__(self):
        self.setup_camera()

    def setup_camera(self):
        self.picam = Picamera2()
        self.picam.start()

    def setup_camera_video(self):
        self.picam = Picamera2()
        
        full_res = self.picam.sensor_resolution
        half_res = [dim // 2 for dim in full_resolution]
        main_stream = {"size": full_resolution, "format": "RGB888"}
        low_res_stream = {"size": (640, 480)}
        video_config = self.picam.create_video_configuration(
            main_stream,
            low_res_stream,
            encode="lores",
            buffer_count=2
        )
        self.picam.configure(video_config)

        encoder = H264Encoder(10000000)
        self.picam.start_recording(encoder, 'test.h264')
        
    def capture_jpeg(self):
        
        buf = BytesIO()
        # self.picam.capture_file(buf, format="jpeg")
        with self.picam.captured_request() as request:
            request.save("main", buf, format="jpeg")
        buf.seek(0)
        return buf

    def capture_array(self):
        buf = BytesIO()
        # img_array = self.picam.capture_array()
        with self.picam.captured_request() as request:
            img_array = request.make_array("main")
            np.save(buf, img_array)
        buf.seek(0)
        return buf
