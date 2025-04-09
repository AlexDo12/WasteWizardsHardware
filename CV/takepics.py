from libcamera import Transform
from picamera2 import Picamera2
from time import sleep
import cv2

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.transform = Transform (vflip=False)
picam2.preview_configuration.main.size = (1640,1232)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
# config = picam2.create_preview_configuration(raw=picam2.sensor_modes[3])
picam2.configure("preview")
picam2.start()

from PIL import Image
import numpy as np


i = 0
SIZE = (640,480)

while True:
    # Capture frame-by-frame
    # filename = "test/image-%d.png" % i
    # image = picam2.capture_file(filename)
    # i += 1

    # sleep(1)
    frame = picam2.capture_array()
    image_from_array = Image.fromarray(frame)
    frame = image_from_array.resize(SIZE)
    frame = np.array(frame)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()