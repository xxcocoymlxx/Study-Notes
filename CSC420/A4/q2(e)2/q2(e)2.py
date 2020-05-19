import numpy as np
from scipy import spatial, cluster
import cv2 as cv
import math
import re
import os
from collections import Counter
from matplotlib import pyplot as plot
import scipy.io as spio

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
        
def segment_image(coords, detections, centers, max_dist):
    
    # The image to return
    ret = np.zeros(coords.shape, int)
    
    # Go through each detection
    for center, (x_left, y_top, x_right, y_bottom, cls) in zip(centers, detections):
        
        # Int-ify each bounding box coordinate for slicing
        yT, yB, xL, xR = int(y_top), int(y_bottom), int(x_left), int(x_right)
        
        # Get slice of coordinates and the center of mass
        coord_slice = coords[yT:yB, xL:xR]
        
        # Compute euclidean distance from center for each coordinate
        center_dists = ((coord_slice - center) ** 2).sum(axis=2) ** 0.5
        
        # Set the points within max_dist to the class color
        ret[yT:yB, xL:xR][center_dists < max_dist] = cls_to_col[cls]
    
    return ret


if __name__ == '__main__':
    test_image_ids =[
    x.strip()
    for x in open("/Users/CYANG/Desktop/A4/data/test/test.txt", "r").readlines()
    ]

    CAR, PERSON, BICYCLE = 0, 1, 2
    cls_lst = [CAR, PERSON, BICYCLE]

    cls_to_name = {
        PERSON : "PERSON",
        BICYCLE : "BICYCLE",
        CAR : "CAR",
    }

    cls_to_col = {
        PERSON:(255, 0, 0), # Blue
        BICYCLE:(255, 255, 0),# Cyan
        CAR:(0, 0, 255), # Red
    }
        
    for img_id in test_image_ids[:3]:
    
        coords = np.load("/Users/CYANG/Desktop/q2(e)1/{}_3d_coords.npy".format(img_id))
        centers = np.load("/Users/CYANG/Desktop/q2(e)1/{}_mass_centers.npy".format(img_id))
        detections = np.load("/Users/CYANG/Desktop/q2(e)1/{}_detections.npy".format(img_id))

        print(detections)
        
        # Segment the image with maximum center-distance of 3 meters
        segmented = segment_image(coords, detections, centers, 3)
        
        display_image(segmented, "q2e-{}-segmentation.png".format(img_id))
