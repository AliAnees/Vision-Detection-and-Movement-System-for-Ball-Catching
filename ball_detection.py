#citation: https://stackoverflow.com/questions/63730808/golf-ball-tracking-in-python-opencv-with-different-color-balls
import cv2
import imutils
import time

#create upper and lower bounds of Hue,Saturation and value based on HSV colour scheme. 
#This is used to identify the colour of the ball
HSVLower = (168, 147, 123)
HSVUpper = (179, 255, 255)

#starts webcam and displays it on a screen of pixel width 640 and height 480
imcap = cv2.VideoCapture(0)
imcap.set(3, 640) # set width as 640
imcap.set(4, 480) # set height as 480

#Defines initial position of the object
x = 0
y = 0

#while loop keeps code running until break command (pressing 'q')
while True:

    _, frame = imcap.read()

    if frame is None:
        break
    #adds gaussian blurr to image
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    width, height = frame.shape[:2]

    #converts blurred image in BRG to HSV for 
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #makss the HSV image in the range defined above (HSVUpper,HSVLower)
    mask = cv2.inRange(hsv, HSVLower, HSVUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #Creates contours around the masked image and approximates a shape
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    #this if statement will only run if there is an object on the screen
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # To see the centroid clearly
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
            cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    output = (int(x),int(y))
    print(output)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()