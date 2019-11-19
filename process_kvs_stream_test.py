import cv2
import boto3
import os


# Part 1 ROI
part_1_start_x, part_1_start_y, part_1_end_x, part_1_end_y = [65, 270, 172, 352]

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


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

    no_of_cnts = len(cnts)



STREAM_NAME="CoolStream"

#video_client = boto3.client('kinesis-video-media',endpoint_url='https://s-5xxxxxx4.kinesisvideo.eu-west-1.amazonaws.com',region_name='eu-west-1')

kinesis_client = boto3.client('kinesisvideo',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_DEFAULT_REGION'])

# # Normal way
# response = kinesis_client.get_data_endpoint(StreamARN='arn:aws:kinesisvideo:eu-west-1:441324442946:stream/CoolStream/1566485232509',APIName='GET_MEDIA')

# HLS way
endpoint = kinesis_client.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamName=STREAM_NAME
)['DataEndpoint']

# video_client = boto3.client('kinesis-video-media',endpoint_url=response['DataEndpoint'])
#
# stream = video_client.get_media(
#     StreamARN='arn:aws:kinesisvideo:eu-west-1:441324442946:stream/CoolStream/1566485232509',
#     StartSelector={'StartSelectorType': 'EARLIEST'})
#
# print (stream)
#
# streamingBody = stream["Payload"]


# streamingBody = stream["Payload"]
# datafeed = streamingBody.read(40000)
#


#s3 = boto3.client('s3')

# # Grab the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
url = kvam.get_hls_streaming_session_url(
    StreamName=STREAM_NAME,
    PlaybackMode="LIVE"
)['HLSStreamingSessionURL']

vcap = cv2.VideoCapture(url)

while(True):
    # Capture frame-by-frame
    ret, frame = vcap.read()

    if frame is not None:
        print("Frame is good")
    else:
        print("Frame is None")
        break

vcap.release()
print ("End of stream")
