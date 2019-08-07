import cv2
import numpy as np
from imutils import contours
import imutils

if __name__ == "__main__":

    image = cv2.imread('./out/protoshape/frame_001521.png')

    start_x = 65
    end_x = 172
    start_y = 270
    end_y = 352
    roi = image[start_y:end_y, start_x:end_x]

    # Write frame
    cv2.imwrite('./out/protoshape/part_1/part1.png', roi)
