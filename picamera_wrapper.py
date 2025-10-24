from io import BytesIO
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, PyavOutput
import time
import socket


class PicameraWrapper:

    def __init__(self):
        self.setup_camera_video()

    def setup_camera(self):
        self.picam = Picamera2()
        self.picam.start()

    def setup_camera_video(self):
        # self.picam = Picamera2()
        
        # full_res = self.picam.sensor_resolution
        # # half_res = [dim // 2 for dim in full_res]
        # main_stream = {"size": (1920, 1080), "format": "RGB888"}
        # controls = {'FrameRate': 30}
        # low_res_stream = {"size": (640, 480)}
        # video_config = self.picam.create_video_configuration(
        #     main_stream,
        #     # low_res_stream,
        #     # encode="lores",
        #     buffer_count=2,
        #     controls=controls,
        # )
        # self.picam.configure(video_config)

        # encoder = H264Encoder(10000000)
        # output = PyavOutput("rtsp://0.0.0.0:8554", format="rtsp")
        # print("Camera starting")
        # self.picam.start_recording(encoder, output)
        # time.sleep(90)
        # print("Camera ended")

        picam2 = Picamera2()
        main = {'size': (1920, 1080), 'format': 'YUV420'}
        controls = {'FrameRate': 30}
        config = picam2.create_video_configuration(main, controls=controls)
        picam2.configure(config)
        encoder = H264Encoder(bitrate=10000000)
        output = PyavOutput("rtsp://0.0.0.0:8554", format="rtsp")
        print("Camera starting")
        picam2.start_recording(encoder, output)
        time.sleep(90)
        print("Camera ended")

        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.connect(("0.0.0.0", 10001))
        # stream = self.sock.makefile("wb")
        
        # self.picam.start_recording(encoder, FileOutput(stream))
        
    def capture_jpeg(self):
        buf = BytesIO()
        with self.picam.captured_request() as request:
            request.save("main", buf, format="jpeg")
        buf.seek(0)
        return buf

    def capture_array(self):
        buf = BytesIO()
        with self.picam.captured_request() as request:
            img_array = request.make_array("main")
            np.save(buf, img_array)
        buf.seek(0)
        return buf
