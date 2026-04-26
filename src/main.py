from picamera2 import Picamera2
import subprocess
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    WIDTH, HEIGHT, FPS = 1280, 720, 30
    cam = Picamera2()

    config = cam.create_video_configuration(
        main={"size": (WIDTH, HEIGHT), format: "BR888"},
        # just for inference
        lores={"size": (WIDTH // 4, HEIGHT // 4), format: "YUV420"},
    )
    cam.configure(config)

    # ffmpeg subprocess
    # formatter ruined the structure
    ffmpeg_proc = subprocess.Popen(
        [
            "ffmpeg",
            "-pix_fmt",  # pixel format
            "brg24",  # for numpy frame support
            "-s",  # size
            f"{WIDTH}x{HEIGHT}",
            "-r",  # framerate
            str(FPS),
            "-i",  # input
            "pipe:0",
            "-c:v",  # encoding!
            "libx264",
            "-preset",
            "ultrafast"  # use least CPU,
            "-tune",
            "zerolatency",  # disables buffering
            "-f",
            "rtsp",  # output format
            f"rtsp://localhost:{os.environ.get('RASPBERRY_PI_RTSP_PORT', 8554)}/stream",
        ],
        stdin=subprocess.PIPE,
    )

    while True:
        try:
            frame = cam.capture_array("main")
            lores = cam.capture_array("lores")
            ffmpeg_proc.stdin.write(frame.tobytes())
        except KeyboardInterrupt:
            break
        finally:
            cam.stop()
            ffmpeg_proc.stdin.close()
            ffmpeg_proc.wait()


if __name__ == "__main__":
    main()
