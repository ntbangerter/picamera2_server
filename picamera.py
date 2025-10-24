from io import BufferedIOBase, BytesIO
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from threading import Condition


class StreamingOutput(BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Picamera:

    def __init__(self):
        self.setup_camera_video()

    def setup_camera(self):
        self.picam = Picamera2()
        self.picam.start()

    def setup_camera_video(self):
        self.picam = Picamera2()

        main_config = {"size": self.picam.sensor_resolution}
        low_res_config = {"size": (640, 480)}

        config = self.picam.create_video_configuration(
            main=main_config,
            lores=low_res_config,
            buffer_count=4,
            controls={"FrameRate": 30},
        )
        self.picam.configure(config)

        self.output = StreamingOutput()
        self.picam.start_recording(
            MJPEGEncoder(),
            FileOutput(self.output),
            stream="lores",
        )

    def generate_frames(self):
        """Generator that yields MJPEG frames for Flask streaming."""
        while True:
            with self.output.condition:
                self.output.condition.wait()
                frame = self.output.frame
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    def capture_jpeg(self, high_res=True):
        stream = "main" if high_res else "lores"
        buf = BytesIO()
        with self.picam.captured_request() as request:
            request.save(stream, buf, format="jpeg")
        buf.seek(0)
        return buf

    def capture_array(self, high_res=True):
        stream = "main" if high_res else "lores"
        buf = BytesIO()
        with self.picam.captured_request() as request:
            img_array = request.make_array(stream)
            np.save(buf, img_array)
        buf.seek(0)
        return buf
