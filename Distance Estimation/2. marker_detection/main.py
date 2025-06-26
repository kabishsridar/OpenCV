import cv2 as cv
from cv2 import aruco
import numpy as np

# dictionary to specify type of the marker
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250) # gets the dictionary type and store it as marker_dict

# detect the marker
param_markers = aruco.DetectorParameters() # detects parameters to be used to detect the marker

# utilizes default camera/webcam driver
cap = cv.VideoCapture(0)

# iterate through multiple frames, in a live video feed
while True:
    ret, frame = cap.read() # reading the camera
    if not ret: # if it is not read, return cannot read
        print("Cannot read")
        break
    # turning the frame to grayscale-only (for efficiency)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # converting to gray scale
    cv.imshow('gray', gray_frame) # displays the window of frame converted to grayscale
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    ) # detecting the corners
    # print(marker_corners)
    # print(marker_IDs)
    # print(reject)
    # getting conrners of markers
    if marker_corners: # if markers corners were found
        print("marker")
        for ids, corners in zip(marker_IDs, marker_corners): # this combines both the id and corners
            cv.polylines( # draws the outline of the aruco marker
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            ) # astype is used so that it will be converted to integers
            corners = corners.reshape(4, 2) # assigning corners
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel() # ravel makes the numpy array into single line
            bottom_left = corners[3].ravel()
            cv.putText( # inserting text of the id 
                frame,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
            print(ids, "  ", corners)
    cv.imshow("frame", frame) # displays the frame
    key = cv.waitKey(1)
    if key == ord("q"): # break when user presses q
        break
cap.release()
cv.destroyAllWindows()