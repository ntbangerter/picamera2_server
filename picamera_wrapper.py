from io import BytesIO
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import socket


class PicameraWrapper:

    def __init__(self):
        self.setup_camera_video()

    def setup_camera(self):
        self.picam = Picamera2()
        self.picam.start()

    def setup_camera_video(self):
        self.picam = Picamera2()
        
        full_res = self.picam.sensor_resolution
        # half_res = [dim // 2 for dim in full_res]
        main_stream = {"size": full_res, "format": "RGB888"}
        low_res_stream = {"size": (640, 480)}
        video_config = self.picam.create_video_configuration(
            main_stream,
            low_res_stream,
            encode="lores",
            buffer_count=2
        )
        self.picam.configure(video_config)

        encoder = H264Encoder(10000000)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", 10001))
        self.sock.listen()

        self.picam.encoders = encoder

        conn, addr = self.sock.accept()
        stream = conn.makefile("wb")
        encoder.output = FileOutput(stream)
        
        self.picam.start_recording(encoder, 'test.h264')

    def start_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", 10001))
        sock.listen()

        
        
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
