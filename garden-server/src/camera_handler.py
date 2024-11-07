import cv2
import threading
import time
import logging
from picamera2 import Picamera2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraHandler:
    def __init__(self):
        self.camera_lock = threading.Lock()
        self.picam2 = Picamera2()
        self.camera_initialized = False
        self._initialize_camera()

    def _initialize_camera(self):
        try:
            config = self.picam2.create_still_configuration()
            self.picam2.configure(config)
            self.picam2.start()
            # Allow camera to warm up
            time.sleep(2)
            self.camera_initialized = True
            logger.info("Camera initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            self.camera_initialized = False

    def capture_picture(self):
      if not self.camera_initialized:
          logger.error("Camera is not initialized.")
          return None

      try:
          with self.camera_lock:
              # Capture the image as a NumPy array in RGB format
              image = self.picam2.capture_array()

              # Convert the image from RGB to BGR
              image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

              # Encode the image as JPEG using OpenCV
              ret, jpeg = cv2.imencode('.jpg', image_bgr)
              if not ret:
                  logger.error("Failed to encode image.")
                  return None

              # Convert the JPEG image to bytes
              img_bytes = jpeg.tobytes()

              return img_bytes
      except Exception as e:
          logger.error(f"Error capturing image: {e}")
          return None

    def close_camera(self):
        try:
            self.picam2.stop()
            logger.info("Camera stopped successfully.")
        except Exception as e:
            logger.error(f"Error stopping camera: {e}")

## Usage example
#if __name__ == "__main__":
#    camera_handler = CameraHandler()
#    image_blob = camera_handler.capture_picture()
#    if image_blob:
#        with open("captured_image.jpg", "wb") as f:
#            f.write(image_blob)
#        logger.info("Image captured and saved successfully.")
#    camera_handler.close_camera()
