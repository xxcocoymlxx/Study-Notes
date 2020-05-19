import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from skimage import data
from PIL import Image

if __name__ == '__main__':
    
    imgname1 = '/Users/CYANG/Desktop/CSC420A3/reference.png'
    imgname2 = '/Users/CYANG/Desktop/CSC420A3/test.png'
    imgname3 = '/Users/CYANG/Desktop/CSC420A3/test2.png'

    sift = cv2.xfeatures2d.SIFT_create()
    img = np.array(Image.open(imgname3), dtype=np.uint8)
    kp,desc = sift.detectAndCompute(img,None)

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(img)

    for i in range(100):
        # Create a Rectangle patch
        rect = patches.Rectangle(kp[i].pt,kp[i].size*10,kp[i].size*10,linewidth=1,edgecolor='r',facecolor='none')

        # Add the patch to the Axes
        ax.add_patch(rect)

    plt.show()

