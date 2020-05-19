import numpy as np
from scipy import spatial, cluster
import cv2 as cv
import math
import re
import os
from collections import Counter
from matplotlib import pyplot as plot
import scipy.io as spio

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

def image_3d_coords(disparity, base_width, focal_length, center_x, center_y):
    """
    Produces an image where each pixel is of form [x, y, z]
    """
    
    # Compute Z/depth first
    z = depth_image(disparity, base_width, focal_length)
    
    # Shift raw coordinates by optical center
    raw_y, raw_x = np.indices(z.shape[:2])
    shifted_y, shifted_x = raw_y - center_y, raw_x - center_x
    
    # d = xL - xR --> xL = d + xR (assuming x-coordinates of disparity are xR)
    # y is assumed to be the same across both images
    yL = shifted_y
    xL = shifted_x + disparity
    
    x = (xL * z) / focal_length
    y = (yL * z) / focal_length
    
    return np.dstack((x, y, z))

def find_closest_mean(vectors, k):
    """
    Returns the mean vector with the smallest magnitude.
    (vectors is assumed to be a k-modal distribution)
    """
    
    # Run K-means
    centroids, labels = cluster.vq.kmeans2(vectors, k)
    
    # Determine magnitude of centroids
    centroid_mags = (centroids ** 2).sum(axis=1) ** 0.5
    closest_label = np.argmin(centroid_mags)
    
    # Return the closest centroid
    return centroids[closest_label]


def centers_of_mass(coords_3d, detections):
    """
    Takes an image of coordinates (each pixel is of form [x, y, z]), 
    and an array of detections each of form 
    [y_top, x_left, y_bottom, x_right, class] 
    
    Computes a numpy array of form [[x, y, z]], where the i-th element 
    is equal to the center of mass of the i-th detection's points
    """
    # Slices of given coordinate matrix (for each detection box)
    slice_inds = (
        row[:4].astype(int) 
        for row in detections
    )
    
    slices = (
        coords_3d[y_top:y_bottom, x_left:x_right]
        #note the order of the params!!!
        for (x_left, y_top, x_right, y_bottom) in slice_inds
    )

    # Flattened (x, y) slices
    flat_slices = (
        s.reshape(np.product(s.shape[:2]), 3)
        for s in slices
    )
    
    # Return closest mean of the bimodal distribution
    return np.array([
        find_closest_mean(vecs, 2)
        for vecs in flat_slices
    ])

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

def load_dets_to_array(detections):
    '''
    given a dictionary loaded from a .mat file
    convert it to an array of the form
    [y_top, x_left, y_bottom, x_right, class] 
    '''
    num_class = detections['dets'].size

    object_lst = []
    for cls in range(num_class):
        for i in range(len(detections['dets'][cls][0])):#every object in each class
            obj = []

            for index in range(4):
                obj.append(detections['dets'][cls][0][i][index])

            if obj != []:
                obj.append(cls)
                obj_array = np.asarray(obj)
                object_lst.append(obj_array)
                
    object_array = np.asarray(object_lst)
    return object_array
    

if __name__ == '__main__':

    base_path = "/Users/CYANG/Desktop/CSC420A4/data/test/"
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
   
    test_image_ids =[
    x.strip()
    for x in open(base_path+"test.txt", "r").readlines()
    ]
    
    for img_id in test_image_ids[:3]:
    
        # Compute 3D coordinates of pixels
        camera_params = get_camera_params(base_path+"calib/{}_allcalib.txt".format(img_id))
        disparity = cv.imread(base_path+"results/{}_left_disparity.png".format(img_id), cv.IMREAD_GRAYSCALE)
        
        baseline, f, px, py = [camera_params[k] for k in ["baseline", "f", "px", "py"]]
        coords = image_3d_coords(disparity, baseline, f, px, py)
        
        # Detections of image
        #detections = np.load("data/test/results/{}_detections.npy".format(img_id))
        dets = spio.loadmat(base_path+"results/dets-test/{}_dets".format(img_id))
        detections = load_dets_to_array(dets)
        np.save("/Users/CYANG/Desktop/q2(e)1/{}_detections.npy".format(img_id), detections)
        
        # Centers of mass for each detection, in order of detections
        mass_centers = centers_of_mass(coords, detections)
        
        # Save the centers of mass and coordinates for each image
        np.save("/Users/CYANG/Desktop/q2(e)1/{}_3d_coords.npy".format(img_id), coords)
        np.save("/Users/CYANG/Desktop/q2(e)1/{}_mass_centers.npy".format(img_id), mass_centers)

