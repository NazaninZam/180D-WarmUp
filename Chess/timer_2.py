# sample code that when blue detected, start a timer that keeps running

'''
This code continuously reads frames from the webcam, converts them to the HSV color space, creates a mask that only shows blue pixels within the specified color range, 
and finds contours in the mask. If any blue contour is detected, the code starts the timer and draws the contours on the frame. If no blue is detected, the timer is reset. 
The code also displays the elapsed time if the timer is started and exits the program when the 'q' key is pressed.
'''

# need to fix the color detetction boundaries usering timer.py code 

import cv2
import time

# Set up the video capture object using the default webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Define the lower and upper bounds for the blue and red colors in HSV color space
blue_lower = (100, 50, 50)
blue_upper = (130, 255, 255)
red_lower = (0, 50, 50)
red_upper = (20, 255, 255)

# Initialize the timers
blue_start_time = 0
red_start_time = 0

while True:
    # Read the frame from the video capture object
    ret, frame = cap.read()

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks that only show blue and red pixels
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # Find contours in the masks
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Check if blue is detected
    if len(blue_contours) > 0:
        # Start the blue timer if it is not already started
        if blue_start_time == 0:
            blue_start_time = time.time()
            print("Blue detected. Blue timer started.")
        # Stop the red timer if it is already started
        if red_start_time != 0:
            red_elapsed_time = time.time() - red_start_time
            print("Red elapsed time: {:.2f} seconds".format(red_elapsed_time))
            red_start_time = 0
        # Draw the blue contours on the frame
        cv2.drawContours(frame, blue_contours, -1, (255, 0, 0), 3)
    # Check if red is detected
    elif len(red_contours) > 0:
        # Start the red timer if it is not already started
        if red_start_time == 0:
            red_start_time = time.time()
            print("Red detected. Red timer started.")
        # Stop the blue timer if it is already started
        if blue_start_time != 0:
            blue_elapsed_time = time.time() - blue_start_time
            print("Blue elapsed time: {:.2f} seconds".format(blue_elapsed_time))
            blue_start_time = 0
        # Draw the red contours on the frame
        cv2.drawContours(frame, red_contours, -1, (0, 0, 255), 3)
    # Reset both timers if no color is detected
    else:
        if blue_start_time != 0:
            blue_elapsed_time = time.time() - blue_start_time
            print("Blue elapsed time: {:.2f} seconds".format(blue_elapsed_time))
            blue_start_time = 0
        if red_start_time != 0:
            red_elapsed_time = time.time() - red_start_time
            print("Red elapsed time: {:.2f} seconds".format(red_elapsed_time))
            red_start_time = 0

    # Display the frame
    cv2.imshow('frame', frame)

    # Check for the 'q' key to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the elapsed time for blue if the blue timer is started
    if blue_start_time != 0:
        blue_elapsed_time = time.time() - blue_start_time
        print("Blue elapsed time: {:.2f} seconds".format(blue_elapsed_time))

    # Display the elapsed time for red if the red timer is started
    if red_start_time != 0:
        red_elapsed_time = time.time() - red_start_time
        print("Red elapsed time: {:.2f} seconds".format(red_elapsed_time))

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
