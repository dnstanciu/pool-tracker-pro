import cv2
import numpy as np
from imutils import contours
import imutils

if __name__ == "__main__":

    cap = cv2.VideoCapture('./in/video2/video2.avi')

    # Video 1 ROI
    #[start_x, start_y, end_x, end_y] = [345, 180, 720, 590]

    # Video 2 ROI
    [start_x, start_y, end_x, end_y] = [274, 482, 586, 832]

    if cap.isOpened() is False:
        print("Error opening video stream or file")

    print("Frame count is " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

    # frame_index = 0
    # while cap.isOpened():
    #     ret_val, image = cap.read()
    #     if image is None:
    #         break
    #     frame_index = frame_index + 1
    #
    #     if frame_index < 6820:
    #         continue
    #
    #     roi = image[start_y:end_y, start_x:end_x]
    #
    #     # Write frame
    #     cv2.imwrite('./out/protoshape/video2/frames/frame' + '_' + f'{frame_index:07}' + '.png', roi)
    #     print ("Processing frame " + str(frame_index))
