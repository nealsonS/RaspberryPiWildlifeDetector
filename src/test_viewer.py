import cv2
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    RPI_IP = os.environ.get("RASPBERRY_IP")
    RTSP_PORT = os.environ.get("RASPBERRY_RTSP_PORT", 8554)
    RTSP_URL = f"rtsp://{RPI_IP}:{RTSP_PORT}/stream"

    # capture stream
    cap = cv2.VideoCapture(RTSP_URL)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Failed to read stream")
            break

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
