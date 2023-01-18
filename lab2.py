#color chnage an image 
import cv2 as cv
image=cv.imread("apple.png")
graypic=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
cv.imwrite("result2.png", graypic)