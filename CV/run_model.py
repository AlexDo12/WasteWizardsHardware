import cv2
from libcamera import Transform
from picamera2 import Picamera2

from lobe import ImageModel
from PIL import Image
import numpy as np

SIZE = (640,480)

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.transform = Transform (vflip=False)
picam2.preview_configuration.main.size = (1640,1232)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
# config = picam2.create_preview_configuration(raw=picam2.sensor_modes[3])
picam2.configure("preview")
picam2.start()

# Load the YOLO11 model
model = ImageModel.load("/home/waste/Desktop/Lobe Model/LobeV1_Trashnet")

while True:
    # Capture frame-by-frame and downsample to target size
    image = Image.fromarray(picam2.capture_array())
    image = image.resize(SIZE)
    frame = np.array(image)
    
    # Run inference on the frame
    results = model.predict(image)
    # print(results.prediction)

    # Add text toframe
    cv2.putText(frame, results.prediction, (50, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Camera", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()