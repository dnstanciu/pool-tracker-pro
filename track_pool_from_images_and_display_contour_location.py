import cv2
import numpy as np
from imutils import contours
import imutils
import glob
import os
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import decimal

def calculateIntersection(a0, a1, b0, b1):
    """
    Calculate intersection between interval.
    Reference: https://stackoverflow.com/a/48537479
    """
    if a0 >= b0 and a1 <= b1: # Contained
        intersection = a1 - a0
    elif a0 < b0 and a1 > b1: # Contains
        intersection = b1 - b0
    elif a0 < b0 and a1 > b0: # Intersects right
        intersection = a1 - b0
    elif a1 > b1 and a0 < b1: # Intersects left
        intersection = b1 - a0
    else: # No intersection (either side)
        intersection = 0

    return intersection

if __name__ == "__main__":

    # Parts Regions of Interest
    parts = [
        # Format: part_start_x, part_start_y, part_end_x, part_end_y
        [65, 270, 172, 352],    # Part 1
        [102, 233, 150, 278],   # Part 2
        [103, 191, 159, 245],   # Part 3
        [111, 148, 162, 195],   # Part 4
        [115, 107, 167, 153],   # Part 5
        [118, 56, 170, 106],    # Part 6
        [164, 279, 226, 338],   # Part 7
        [161, 228, 225, 289],   # Part 8
        [166, 180, 231, 245],   # Part 9
        [169, 137, 230, 197],   # Part 10
        [170, 90, 232, 148],    # Part 11
        [174, 48, 233, 99],     # Part 12
    ]

    image_file_list = []
    # for filename in glob.glob('./out/protoshape/frames_test_multiple/*.png'):
    for filename in glob.glob('./out/protoshape/video2/frames/*.png'):
        image_file_list.append(filename)

    image_file_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    for image_file_path in image_file_list:
        print("Processing: " + image_file_path)
        input("Press Enter to continue...")

        # Load an color image in grayscale
        #image = cv2.imread('./out/protoshape/frames/frame_001521.png')
        image = cv2.imread(image_file_path)


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # TODO convert RGB to HSV for better light sensitivity
        # hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        # h, s, v1 = cv2.split(hsv1)


        # Blur to remove noise (radius must be ODD)
        gray = cv2.GaussianBlur(gray, (5, 5), 0) # 21,21
        # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        # image = orig.copy()
        # cv2.circle(image, maxLoc, 21, (255, 0, 0), 2)

        # threshold the image to reveal light regions in the blurred image
        thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)[1]
        # display the results of the naive attempt
        #cv2.imshow("Naive", image)

        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        # thresh = cv2.erode(thresh, None, iterations=2)
        # thresh = cv2.dilate(thresh, None, iterations=4)
        thresh = cv2.erode(thresh, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)

        # cv2.imwrite('./out/protoshape/interim/denoised2.png', thresh)


        # Contours
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        cnts = imutils.grab_contours(cnts)
        if len(cnts) != 0:
            sorted_contours = sorted(cnts, key=cv2.contourArea, reverse=True)

            largest_contour = sorted_contours[0]

            # Get area
            area = cv2.contourArea(largest_contour)

            # Get average intensity
            contour_mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(contour_mask, largest_contour, -1, 255, -1)
            mean = cv2.mean(gray, mask=contour_mask)

            # Get radius length TODO: or use perimeter aka length or both?
            ((cX, cY), radius) = cv2.minEnclosingCircle(largest_contour)

            cv2.drawContours(image, [largest_contour], -1, (0, 0, 255), 1)
            #cv2.rectangle(image, (part_1_start_x, part_1_start_y), (part_1_end_x, part_1_end_y), (0, 255, 0))

        cv2.imwrite('./out/protoshape/interim/the_contour.png', image)
