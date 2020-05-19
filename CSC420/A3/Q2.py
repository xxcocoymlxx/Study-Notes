import numpy as np
from scipy import spatial
import cv2 as cv
import math
from matplotlib import pyplot as plot

def make_match_rows(x, y, x_prime, y_prime):
    """
    Makes two rows of match matrix A
    """
    return np.array([
        [x, y, 1, 0, 0, 0, -x_prime * x, -x_prime * y, -x_prime],
        [0, 0, 0, x, y, 1, -y_prime * x, -y_prime * y, -y_prime]
    ], dtype=float)

def make_match_matrix(matches):
    """
    Given an iterable of matches, where each match has the form (x, y, x_prime, y_prime),
    make the matrix A.
    """
    return np.vstack([
        make_match_rows(x, y, x_prime, y_prime) 
        for (x, y, x_prime, y_prime) in matches
    ])

def solve_homography(matches):
    """
    Given an iterable of matches, where each match has the form (x, y, x_prime, y_prime),
    compute the best homography h_hat (the eigenvector of A^TA with smallest eigenvalue).
    
    Transform this eigenvector into a 3x3 matrix
    """
    A = make_match_matrix(matches)
    eig_vals, eig_vecs = np.linalg.eig(A.transpose() @ A)
    
    # Get eigenvector with smallest eigenvalue (vectors are arranged vertically)
    homography_vec = eig_vecs[:, np.argmin(eig_vals)]
    
    # Reshape the homography into a matrix
    return homography_vec.reshape(3, 3)


def apply_homography(homography, cartesian_coords):
    """
    Applies homography to each coordinate in cartesian_coords.
    Returns an array of form [[x, y]], where (x, y) are the 
    homography-transformed cartesian coordinates.
    """
    # Turn the cartesian coordinates into homogeneous coordinates (columns are [x, y, 1])
    homo_coords = np.array([
        (*coord, 1) 
        for coord in cartesian_coords
    ], dtype=float).transpose()
    
    # Each column is now of form ([ax', ay', a])
    transformed = homography @ homo_coords
    
    # Divide out the a's
    normalized = transformed[:2, :] / transformed[2, :]
    
    return normalized.transpose()


if __name__ == '__main__':
    door_paper = cv.imread("/Users/CYANG/Desktop/CSC420A3/door.jpeg")

    # Original coordinates of paper corners (X=21.6cm, Y=28cm)
    #corrdinates are in Top Left,Top Right,Bottom Left,Bottom Right order
    paper_cm_coords = np.array([(0, 0),(21.6, 0),(0, 28),(21.6, 28)], dtype=float)

    #Pixel coordinates of paper corners
    #I used cv2.imshow() to display the image
    #and it show the coordinates when you drag your mouse
    #around on the image
    paper_pixel_coords = np.array([(656, 647),(759, 651),(654, 784),(755, 796),], dtype=float)

    # Solve the homography that maps pixels to cm
    pixels_to_cm = solve_homography([(*a, *b) for (a, b) in zip(paper_pixel_coords, paper_cm_coords)])

    # Pixel coordinates of door corners
    door_pixel_coords = np.array([(396, 232),(761, 173),(409, 1135),(730, 1239)], dtype=float)

    # Map the door pixels into cm space
    door_cm_coords = apply_homography(pixels_to_cm, door_pixel_coords)

    # Figure out the width/height of the door
    door_x, door_y = door_cm_coords.transpose()
    door_width = max(door_x) - min(door_x)
    door_height = max(door_y) - min(door_y)
    

    print("Width")
    print("Estimate:{} cm".format(round(door_width, 2)))
    print("")

    print("Height")
    print("Estimate:{} cm".format(round(door_height, 2)))
    


