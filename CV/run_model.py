import cv2
from libcamera import Transform
from picamera2 import Picamera2

from lobe import ImageModel

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.transform = Transform (vflip=False)
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLO11 model
model = ImageModel.load("/home/waste/Desktop/Lobe Model/LobeV1_Trashnet")

while True:
    # Capture frame-by-frame
    image = picam2.capture_image()
    frame = picam2.capture_array()
    
    # Run YOLO11 inference on the frame
    results = model.predict(image)
    print(results.prediction)

    # Visualize the results on the frame
    # annotated_frame = results.plot()
    # heatmap = model.visualize(image)
    # heatmap.show()

    # Text parameters
    text = results.prediction
    org = (50, 100)  # Position of the text (bottom-left corner)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1
    color = (0, 0, 255)  # White color in BGR
    thickness = 2

    # Add text to the image
    cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Camera", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()