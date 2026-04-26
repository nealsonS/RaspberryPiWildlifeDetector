from picamera2 import Picamera2
import subprocess
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    WIDTH, HEIGHT, FPS = 1280, 720, 30
    cam = Picamera2()

    config = cam.create_video_configuration(
        main={"size": (WIDTH, HEIGHT), "format": "BGR888"},
        lores={"size": (WIDTH // 4, HEIGHT // 4), "format": "YUV420"},
    )
    cam.configure(config)

    RTSP_URL = (
        f"rtsp://localhost:{os.environ.get('RASPBERRY_PI_RTSP_PORT', 8554)}/stream"
    )

    ffmpeg_proc = subprocess.Popen(
        [
            "ffmpeg",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{WIDTH}x{HEIGHT}",
            "-r",
            str(FPS),
            "-i",
            "pipe:0",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-tune",
            "zerolatency",
            "-f",
            "rtsp",
            RTSP_URL,
        ],
        stdin=subprocess.PIPE,
    )
    print(f"Streaming on:\n{RTSP_URL}")

    try:
        while True:
            frame = cam.capture_array("main")
            ffmpeg_proc.stdin.write(frame.tobytes())
    except KeyboardInterrupt:
        pass
    finally:
        cam.stop()
        ffmpeg_proc.stdin.close()
        ffmpeg_proc.wait()


if __name__ == "__main__":
    main()
