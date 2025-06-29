import cv2 as cv
from cv2 import aruco
import numpy as np
from picamera2 import Picamera2
import time
import turtle as t
from turtle import Turtle

tur = t.Screen()
tur.title('Line Graph')
tur.bgcolor('white')
display = t.Turtle()

# dictionary to specify type of the marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250) # gets the dictionary type and store it as marker_dict

# detect the marker
param_markers = aruco.DetectorParameters_create() # detects parameters to be used to detect the marker

# utilizes default camera/webcam driver
picam2 = Picamera2()

config = picam2.create_preview_configuration(main={"size": (640, 480)}, lores={"size": (320, 240)}, display="lores")
picam2.configure(config)

picam2.start()
time.sleep(0.01)
cv.namedWindow("RPI", cv.WINDOW_NORMAL)
x = []
y = []
# iterate through multiple frames, in a live video feed
while True:
    frame_org = picam2.capture_array("main")
    # frame_org = cv.flip(frame, 1)
    frame_bgr = cv.cvtColor(frame_org, cv.COLOR_RGB2BGR)
    #cv.imshow("RPI live", frame_bgr)
    # turning the frame to grayscale-only (for efficiency)
    gray_frame = cv.cvtColor(frame_org, cv.COLOR_BGR2GRAY) # converting to gray scale
    #cv.imshow('gray', gray_frame) # displays the window of frame converted to grayscale
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    ) # detecting the corners
    if marker_corners:
        # print(marker_corners[0][0][0][0])
        x.append(marker_corners[0][0][0][0])
        y.append(marker_corners[0][0][0][1])
        display.goto(marker_corners[0][0][0][0], marker_corners[0][0][0][1])

    # print(marker_IDs)
    # print(reject)
    # getting conrners of markers
    if marker_IDs is not None and marker_corners is not None: # if markers corners were found
        # print("marker")
        for ids, corners in zip(marker_IDs, marker_corners): # this combines both the id and corners
            cv.polylines( # draws the outline of the aruco marker
                frame_org, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            ) # astype is used so that it will be converted to integers
            corners = corners.reshape(4, 2) # assigning corners
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel() # ravel makes the numpy array into single line
            bottom_left = corners[3].ravel()
            cv.putText( # inserting text of the id 
                frame_org,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )

    cv.imshow("frame", frame_org) # displays the frame
    key = cv.waitKey(1)
    if key == ord("q"): # break when user presses q
        break

for i in range(len(x)):
    print(f"x: {x[i]}, y: {y[i]}")
picam2.stop()
cv.destroyAllWindows()