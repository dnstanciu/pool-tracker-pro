import cv2
import numpy as np
from imutils import contours
import imutils

if __name__ == "__main__":

    # Load an color image in grayscale
    image = cv2.imread('./in/protoshape_laser_tracking.png')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur to remove noise (radius must be ODD)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # image = orig.copy()
    # cv2.circle(image, maxLoc, 21, (255, 0, 0), 2)

    # threshold the image to reveal light regions in the blurred image
    thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)[1]
    # display the results of the naive attempt
    #cv2.imshow("Naive", image)

    # perform a series of erosions and dilations to remove
    # any small blobs of noise from the thresholded image
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    # Contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        cnts = imutils.contours.sort_contours(cnts)[0]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        # Just get the largest contour
        cnt = cnts[0]
        area = cv2.contourArea(cnt)

        cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)
        # ((cX, cY), radius) = cv2.minEnclosingCircle(cnt)
        # cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)

        cv2.putText(image, str(area), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Just get the largest contour
        cnt = cnts[2]
        area = cv2.contourArea(cnt)

        cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)
        # ((cX, cY), radius) = cv2.minEnclosingCircle(cnt)
        # cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)

        # cv2.putText(image, str(area), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Just get the largest contour
        cnt = cnts[3]
        area = cv2.contourArea(cnt)

        cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)
        # ((cX, cY), radius) = cv2.minEnclosingCircle(cnt)
        # cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)

        # cv2.putText(image, str(area), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Write frame
    cv2.imwrite('./out/protoshape/MTC.png', image)
    
