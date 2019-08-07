import cv2
import numpy as np
from imutils import contours
import imutils

if __name__ == "__main__":

    cap = cv2.VideoCapture('./in/video_ai.mp4')

    frame_index = 0
    if cap.isOpened() is False:
        print("Error opening video stream or file")

    while cap.isOpened():
        ret_val, image = cap.read()
        if image is None:
            break
        frame_index = frame_index + 1

        start_x = 345
        start_y = 180
        end_x = 720
        end_y = 590
        roi = image[start_y:end_y, start_x:end_x]

        # Write frame
        cv2.imwrite('./out/protoshape/frame' + '_' + f'{frame_index:06}' + '.png', roi)
        print ("Processing frame " + str(frame_index))
