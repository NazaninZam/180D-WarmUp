# https://www.tutorialspoint.com/how-to-create-a-timer-using-tkinter
#https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/ 

# sample code that when blue detected, start a timer that keeps running

'''
This code continuously reads frames from the webcam, converts them to the HSV color space, creates a mask that only shows blue pixels within the specified color range, 
and finds contours in the mask. If any blue contour is detected, the code starts the timer and draws the contours on the frame. If no blue is detected, the timer is reset. 
The code also displays the elapsed time if the timer is started and exits the program when the 'q' key is pressed.
'''
#add a kmeans and average + 10% error margin 
# set specific regions for it to detect the color 
# can have "calibration" with different lighting and it'll now still work
# need to fix the color detetction boundaries usering timer.py code 

import cv2
import time
import numpy as np
import tkinter as tk

# Set up tkinter window
root = tk.Tk()
root.geometry("200x100")

# Create a label for displaying time
label = tk.Label(root, text="", font=("Arial", 30))
label.pack()

# Set up the video capture object using the default webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # needed cvs.CAP_DSHOW for external camera 

# Start timer function
def start_timer():
    global start_time
    start_time = time.time()

# Initialize the timers
blue_start_time = 0
red_start_time = 0

while True:
    # Read the frame from the video capture object
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks that only show blue and red pixels

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    kernal = np.ones((5, 5), "uint8")

    #for blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask = blue_mask)

    #for red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(frame, frame,mask = red_mask)
        
    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours): 
        
        blue_area = cv2.contourArea(contour)
        
        if(blue_area > 300):		
            #x, y, w, h = cv2.boundingRect(contour)
            x, y, w, h = 0, 0, 100, 100 
            imageFrame = cv2.rectangle(frame, (x, y),(x + w, y + h),(255, 0, 0), 2)
			# Start the blue timer if it is not already started
            
            cv2.putText(imageFrame, "Blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))
            
            if blue_start_time == 0:
                blue_start_time = time.time()
                print("Blue detected. Blue timer started.")
                # Stop the red timer if it is already started
                if red_start_time != 0:
                    red_elapsed_time = time.time() - red_start_time
                    print("Red elapsed time: {:.2f} seconds".format(red_elapsed_time))
                    red_start_time = 0
                start_timer()


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
    for pic, contour in enumerate(contours):
        red_area = cv2.contourArea(contour)
        if(red_area > 300):
            #x, y, w, h = cv2.boundingRect(contour)
            x, y, w, h = 0, 0, 100, 100 
            imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			
            cv2.putText(imageFrame, "Red", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))	
            # Start the red timer if it is not already started
            if red_start_time == 0:
                red_start_time = time.time()
                print("Red detected. Red timer started.")
            # Stop the blue timer if it is already started
            if blue_start_time != 0:
                blue_elapsed_time = time.time() - blue_start_time
                print("Blue elapsed time: {:.2f} seconds".format(blue_elapsed_time))
                blue_start_time = 0  

    '''
        # Check if blue is detected
        if blue_area > 0:
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
            cv2.drawContours(frame, blue_area, -1, (255, 0, 0), 3)

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


    '''

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

# Update label with elapsed time
def update_label():
    elapsed_time = time.time() - start_time
    label.config(text=str(round(elapsed_time, 2)))
    root.after(10, update_label)

update_label()

root.mainloop()