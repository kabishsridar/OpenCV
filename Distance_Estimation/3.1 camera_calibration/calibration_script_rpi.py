import cv2 as cv # imporing required modules
import os
import numpy as np

# Chess/checker board size, dimensions
CHESS_BOARD_DIM = (9, 6) # the dimension of chessboard(there should be exact dimension where we caliberate and we capture)

# The size of squares in the checker board design.
SQUARE_SIZE = 22  # millimeters (change it according to printed size)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

calib_data_path = "../calib_data_rpi"
CHECK_DIR = os.path.isdir(calib_data_path)

# saving the image / camera calibration data

if not CHECK_DIR: # checks whether the Dir is presented
    os.makedirs(calib_data_path)
    print(f'"{calib_data_path}" Directory is created')

else:
    print(f'"{calib_data_path}" Directory already Exists.')

# prepare object points, i.e. (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# will be np.zeros(9 * 6, 3) and converted to float will return 0s of 54 rows and 3 columns
obj_3D = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)

obj_3D[:, :2] = np.mgrid[0 : CHESS_BOARD_DIM[0], 0 : CHESS_BOARD_DIM[1]].T.reshape(
    -1, 2
)
obj_3D *= SQUARE_SIZE
print(obj_3D) # returns the value of the matrix

# Arrays to store object points and image points from all the given images.
obj_points_3D = []  # 3d point in real world space
img_points_2D = []  # 2d points in image plane

# The images directory path
image_dir_path = "//home//kabish//python_projects//opencv//Distance_Estimation//3.1 camera_calibration//images_rpi2"

files = os.listdir(image_dir_path)  # list of names of all the files present
for file in files:
    print(file) # displays the file names in the folder
    imagePath = os.path.join(image_dir_path, file)
    # print(imagePath)

    image = cv.imread(imagePath) # reads the image
    grayScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # converting to grayscale
    ret, corners = cv.findChessboardCorners(image, CHESS_BOARD_DIM, None) # detects the chess board corners
    if ret == True:
        obj_points_3D.append(obj_3D)
        corners2 = cv.cornerSubPix(grayScale, corners, (3, 3), (-1, -1), criteria)
        img_points_2D.append(corners2)

        img = cv.drawChessboardCorners(image, CHESS_BOARD_DIM, corners2, ret)

cv.destroyAllWindows()
# h, w = image.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    obj_points_3D, img_points_2D, grayScale.shape[::-1], None, None
) # caliberation part
print("calibrated")

print("dumping the data into one files using numpy ")
np.savez(
    f"{calib_data_path}/MultiMatrix",
    camMatrix=mtx,
    distCoef=dist,
    rVector=rvecs,
    tVector=tvecs,
) # creating a file and storing all the datas to the file named MultiMatrix

print("-------------------------------------------")

print("loading data stored using numpy savez function\n \n \n")

data = np.load(f"{calib_data_path}/MultiMatrix.npz")

camMatrix = data["camMatrix"]
distCof = data["distCoef"]
rVector = data["rVector"]
tVector = data["tVector"]

print("loaded calibration data successfully")