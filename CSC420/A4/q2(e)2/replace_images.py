import numpy as np
from scipy import spatial, cluster
import scipy.io as spio
import cv2 as cv
import math
import re
import os
from collections import Counter
from matplotlib import pyplot as plot

def display_image(img, file_name=None, save_norm=True, save_type=np.uint8):
    """
    Shows an image (max-min normalized to 0-255), and saves it if a filename is given
    save_norm = whether to save the normalized image
    save_type = what datatype to save the image as
    """

    flt_img = img.astype(float)
    img_max, img_min = np.max(flt_img), np.min(flt_img)
    norm = (((flt_img - img_min) / (img_max - img_min)) * 255).astype(np.uint8)

    if len(img.shape) == 2:
        plot.imshow(norm, cmap='gray')
    elif (len(img.shape) == 3):
        plot.imshow(cv.cvtColor(norm, cv.COLOR_BGR2RGB))
    plot.show()

    to_save = norm if save_norm else flt_img
    if file_name:
        cv.imwrite(file_name, to_save)
        
if __name__ == '__main__':
    img1 = cv.imread('/Users/CYANG/Desktop/A4/q2(e)2/replace2.png')
    img2 = cv.imread('/Users/CYANG/Desktop/A4/q2(e)2/replace1.png')

    #cv.imshow('image',img1)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    
    img1H, img1W,_ = img1.shape
    
    R = np.zeros((img1H, img1W), int)
    G = np.zeros((img1H, img1W), int)
    B = np.zeros((img1H, img1W), int)
    img1_R = img1[:,:,0]
    img1_G = img1[:,:,1]
    img1_B = img1[:,:,2]
    img2_R = img2[:,:,0]
    img2_G = img2[:,:,1]
    img2_B = img2[:,:,2]

    for i in range(img1H):
        for j in range(img1W):
            if j < 800:
                R[i][j] = img1_R[i][j]
            else:
                R[i][j] = img2_R[i][j]

    for i in range(img1H):
        for j in range(img1W):
            if j < 800:
                G[i][j] = img1_G[i][j]
            else:
                G[i][j] = img2_G[i][j]

    for i in range(img1H):
        for j in range(img1W):
            if j < 800:
                B[i][j] = img1_B[i][j]
            else:
                B[i][j] = img2_B[i][j]

    rgb = np.dstack((R,G,B))
    display_image(rgb, "test.png")
    
    
