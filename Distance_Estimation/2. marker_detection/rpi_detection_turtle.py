import cv2 as cv
from cv2 import aruco
import numpy as np
from picamera2 import Picamera2
import time
import turtle as t
from PIL import Image, ImageTk

# Set up the Turtle graphics window
tur = t.Screen()
tur.title('ArUco Detection')
tur.bgcolor('white')
display = t.Turtle()

# Dictionary to specify type of the marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

# Detect the marker
param_markers = aruco.DetectorParameters_create()

# Utilize the default camera/webcam driver
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)}, lores={"size": (320, 240)}, display="lores")
picam2.configure(config)

picam2.start()
time.sleep(0.01)

# Create a canvas for displaying the video frames
canvas = t.getcanvas() # browser
frame_image = None
x = []
y = []
# Iterate through multiple frames in a live video feed
while True:
    frame = picam2.capture_array("main")
    frame_bgr = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect markers
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    if marker_corners:
        x.append(marker_corners[0][0][0][0])
        y.append(marker_corners[0][0][0][1])
        for ids, corners in zip(marker_IDs, marker_corners):
            corners = corners.reshape(4, 2).astype(int)
            top_right = corners[0].ravel()

            # Display the ID in the Turtle graphics window
            display.clear()  # Clear previous text
            display.goto(0, 0)  # Move to the center of the screen
            display.write(f"ID: {ids[0]}", align="center", font=("Arial", 20, "normal"))

            # Draw the outline of the ArUco marker
            cv.polylines(frame_bgr, [corners], True, (0, 255, 255), 4, cv.LINE_AA)
            cv.putText(frame_bgr, f"id: {ids[0]}", top_right, cv.FONT_HERSHEY_PLAIN, 1.3, (200, 100, 0), 2, cv.LINE_AA)

    # Convert the frame to a format suitable for Turtle
    frame_rgb = cv.cvtColor(frame_bgr, cv.COLOR_BGR2RGB)  # Convert to RGB
    frame_image = Image.fromarray(frame_rgb)  # Create an image from the array # browser
    frame_image = frame_image.resize((840, 680))  # Resize to fit the Turtle window
    frame_tk = ImageTk.PhotoImage(frame_image)  # Convert to PhotoImage # browser
    # for i in range(len(x)):
        #display.write(x[i], y[i])
        # print(x[i], y[i])
        # display.clear()
        # display.write(f"x : {x[i]}, y : {y}", font=("Arial", 15, "bold"))

    # Update the canvas with the new image
    canvas.create_image(0, 0, anchor='nw', image=frame_tk)  # Use 'nw' for north-west anchor
    canvas.update()  # Refresh the canvas

    # Check for exit key
    key = cv.waitKey(1)
    if key == ord("q"):  # Break when user presses 'q'
        break

# Clean up
picam2.stop()
t.done()
cv.destroyAllWindows()