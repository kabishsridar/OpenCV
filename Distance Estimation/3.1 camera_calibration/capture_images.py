import cv2 as cv # importing the required modules
import os

Chess_Board_Dimensions = (9, 6) # assigning the dimensions of the chess board

n = 0  # image counter

# checks images dir is exist or not
image_path = "images"

Dir_Check = os.path.isdir(image_path) # checks whether the path is presented

if not Dir_Check:  # if directory does not exist, a new one is created
    os.makedirs(image_path)
    print(f'"{image_path}" Directory is created')
else:
    print(f'"{image_path}" Directory already exists.')

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# the termination criteria 
# (will terminate when the iteration reaches 30 or the movement of corner is less than 0.001 px)

def detect_checker_board(image, grayImage, criteria, boardDimension): # function to detect the board
    ret, corners = cv.findChessboardCorners(grayImage, boardDimension) # gets the position of corners of chessboard
    if ret == True: # if read
        corners1 = cv.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)
        image = cv.drawChessboardCorners(image, boardDimension, corners1, ret) # draws circle in the edge

    return image, ret


cap = cv.VideoCapture(0) # captures the frame

while True: # captures continuously until break (q)
    _, frame = cap.read() # reads the frame
    copyFrame = frame.copy() # copies the frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # converting to gray scale

    image, board_detected = detect_checker_board(
        frame, gray, criteria, Chess_Board_Dimensions
    ) # detects chessboard by calling the function
    # print(ret)
    cv.putText(
        frame,
        f"saved_img : {n}",
        (30, 40),
        cv.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv.LINE_AA,
    ) # displays the information saved image

    cv.imshow("frame", frame) # displays the original window
    # copyframe; without augmentation
    cv.imshow("copyFrame", copyFrame) # displays the copied window

    key = cv.waitKey(1)

    if key == ord("q"):
        break
    if key == ord("s") and board_detected == True: # if s is presed
        # the checker board image gets stored
        cv.imwrite(f"{image_path}/image{n}.png", copyFrame) # the original chessboard will be stored

        print(f"saved image number {n}")
        n += 1  # the image counter: incrementing
cap.release()
cv.destroyAllWindows()

print("Total saved Images:", n)
