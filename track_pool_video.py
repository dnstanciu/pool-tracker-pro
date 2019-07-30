import cv2
import numpy as np
from imutils import contours
import imutils

if __name__ == "__main__":

    cap = cv2.VideoCapture('./in/video_ai.mp4')

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()

    frame_index = 0
    if cap.isOpened() is False:
        print("Error opening video stream or file")

    while cap.isOpened():
        ret_val, image = cap.read()
        if image is None:
            break
        frame_index = frame_index + 1

        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Blur to remove noise (radius must be ODD)
        gray = cv2.GaussianBlur(gray, (41, 41), 0)
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


        # Detect blobs.
        # keypoints = detector.detect(image)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        # for marker in keypoints:
        #     img2 = cv2.drawMarker(img2, tuple(int(i) for i in marker.pt), color=(0, 255, 0))

        #im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


        #cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # cv2.imshow('tf-pose-estimation result', image)

        # Write frame
        cv2.imwrite('./out/protoshape/frame' + '_' + f'{frame_index:04}' + '.png', image)

        #fps_time = time.time()
        # if cv2.waitKey(1) == 27:
        #     break
        print ("Processing frame " + str(frame_index))
