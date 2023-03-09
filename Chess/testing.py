#cant open camera and tkinter at the same time for debugging
#need threading module
'''
#countdown timer
import time

def countdown(n):
    while n > 0:
        print(n)
        time.sleep(1)
        n -= 1
    print("Countdown complete!")

countdown(10)
'''
'''

from tkinter import *
import cv2
import tkinter as tk
import numpy as np
import time
import threading

ui = Tk()
ui.state('normal')
canvas = tk.Canvas()
canvas.pack(fill = 'both', expand = True)


def video_stream():
  video = cv2.VideoCapture(0)
  a = 0
  while True:
    a+= 1
    check, frame = video.read()
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
  video.release()
  cv2.destroyAllWindows

th= threading.Thread(target=video_stream) #initialise the thread
th.setDaemon(True)
th.start() #start the thread

ui.mainloop() #Run your UI
'''

'''
import cv2
import numpy as np
import tkinter as tk
import time

# Set up tkinter window
root = tk.Tk()
root.geometry("200x100")

# Create a label for displaying time
label = tk.Label(root, text="", font=("Arial", 30))
label.pack()

# Define blue color range
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Set up video capture
cap = cv2.VideoCapture(0)

# Start timer function
def start_timer():
    global start_time
    start_time = time.time()

# Check for blue color and start timer
while True:
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for blue color range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Check if blue color is detected
    if len(contours) > 0:
        # Start the timer
            # Display video frame in a window
        cv2.imshow("Video Frame", frame)
        start_timer()
        break



    # Check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Destroy OpenCV windows and release video capture
cv2.destroyAllWindows()
cap.release()

# Update label with elapsed time
def update_label():
    elapsed_time = time.time() - start_time
    label.config(text=str(round(elapsed_time, 2)))
    root.after(10, update_label)

update_label()

# Start tkinter event loop
root.mainloop()
'''

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
width = cap.get(3)
height = cap.get(4)

while(1):
    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV

    lower_hsv = np.array([36, 50, 70])
    upper_hsv= np.array([89, 255, 255])
    # Threshold the HSV image 
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)

    _,thresh = cv.threshold(mask,127,255,0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    if len(contours):
        cont = max(contours, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cont)
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()