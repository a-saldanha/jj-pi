# Test individual cameras
from picamera2 import Picamera2
import time

def test_cameras():
    # Test first camera
    cam0 = Picamera2(0)
    cam0.start_preview()
    cam0.start()
    time.sleep(2)
    cam0.capture_file("test_cam0.jpg")
    cam0.stop()
    cam0.close()
    
    # Test second camera
    cam1 = Picamera2(1)
    cam1.start_preview()
    cam1.start()
    time.sleep(2)
    cam1.capture_file("test_cam1.jpg")
    cam1.stop()
    cam1.close()

test_cameras()