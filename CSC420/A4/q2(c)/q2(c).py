import numpy as np
from scipy import spatial, cluster
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
        
def depth_image(disparity_image, base_width, focal_length):
    """
    Creates a depth image using a disparity image and 
    some camera parameters (base width, focal length)
    """
    #using the formula stated in lecture slides
    numerator = base_width * focal_length
    
    # Avoid "division by zero" errors
    denominator = disparity_image.astype(float)
    denominator[denominator == 0] = 1
    result = numerator / denominator
    
    # Set what should have been infinity to maximum
    result[denominator == 0] = np.max(result)
    
    return result

def get_camera_params(param_path):
    """
    Returns dictionary of camera parameter values 
    stored in the file at param_path
    """   
    # Lines of the file are of form (param : value)
    line_regex = re.compile(r"(?P<param>(\w+)):(\s+)(?P<value>(\d+(\.\d+)?))")
    
    with open(param_path, "r") as file:
    
        # Matching the regex to the lines in the file
        matches = (line_regex.match(line) for line in file.readlines())
        
        # Organize the parameters into a dictionary for easy access
        return {
            match.group("param") : float(match.group("value"))
            for match in matches
        }

if __name__ == '__main__':
   test_image_ids =[
    x.strip()
    for x in open("/Users/CYANG/Desktop/CSC420A4/data/test/test.txt", "r").readlines()
   ]


   base_path = "/Users/CYANG/Desktop/CSC420A4/data/test/"
   for img_id in test_image_ids[:3]:#only use the first 3 images
       #txt files
       camera_params = get_camera_params(base_path + "calib/{}_allcalib.txt".format(img_id))
       disparity_img = cv.imread(base_path + "results/{}_left_disparity.png".format(img_id), cv.IMREAD_GRAYSCALE)
       depth_img = depth_image(disparity_img, camera_params["baseline"], camera_params["f"])
        
       display_image(depth_img, "q2c-{}-depth.png".format(img_id), save_norm=False, save_type=np.float32)

       
