'''
    Resources:
        https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
'''

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

# set up plot for histogram
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
cap = cv.VideoCapture(0)

while True:
  
    ret, frame = cap.read()
    cv.rectangle(frame,(50,50),(2200,2200),(0,255,0),2)

    cv.imshow('frame', frame)
    
    frame = frame.reshape((frame.shape[0] * frame.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(frame)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    plt.axis("off")
    plt.imshow(bar)
    plt.show()
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()