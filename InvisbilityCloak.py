
import cv2
import numpy as np
import time

# initialize webcam
    # 0 stands for default camera, video object is now ready to start pulling frames from the camera
    # needs to sleep to give you time to move out of the frame
video = cv2.VideoCapture(0) 
time.sleep(3)

# capture static picture of your background
    # reads 30 frames from the webcam
        # checking if it worked (success) and the frame itself (bg_frame) which is a numpy array of pixels
bg_frame = 0
for _ in range(30):
    success, bg_frame = video.read()
    
# flip background using numpy
    # flipping across vertical axis (which is 1)
bg_frame = np.flip(bg_frame, axis = 1)



while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    frame = np.flip(frame, axis = 1)

    # convert from RGB (red, green, blue) into HSV (hue, saturation, value) which is easier to detect specific colors
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blurred_hsv = cv2.GaussianBlur(hsv_img, (35,35), 0)
    
    # red_lower_1 = np.array([0,120, 70]) ([120, 70, 0])
    # red_upper_1 = np.array([10, 255, 255]) ([255, 255, 10])
    # mask_red1 = cv2.inRange(hsv_img, red_lower_1, red_upper_1)

    # red_lower_2 = np.array([170,120, 70])
    # red_upper_2 = np.array([180, 255, 255])
    # mask_red2 = cv2.inRange(hsv_img, red_lower_2, red_upper_2)
    # full_mask = mask_red1 + mask_red2
    

    # Define the range for blue color in HSV
    blue_lower = np.array([90, 110, 60])
    blue_upper = np.array([140, 255, 255])

    # Create a mask for blue color
    full_mask = cv2.inRange(hsv_img, blue_lower, blue_upper)
    
    # clean up noise
    full_mask = cv2.morphologyEx(full_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))

    frame[np.where(full_mask==255)] = bg_frame[np.where(full_mask == 255)]


    # showing final output
    cv2.imshow("Magic Window", frame)

    if cv2.waitKey(10) == 27:
        break
