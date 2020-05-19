import cv2
import numpy as np
from matplotlib import pyplot as plot
import matplotlib.patches as patches
from skimage import data
from PIL import Image
from scipy import spatial

# Shows an image, and saves it if a filename is given
def display_image(img, file_name=None):
    
    flt_img = img.astype(float)
    img_max, img_min = np.max(flt_img), np.min(flt_img)
    
    norm_img = (((flt_img - img_min) / (img_max - img_min)) * 255).astype(np.uint8)
    
    if len(img.shape) == 2:
        plot.imshow(norm_img, cmap='gray')
    elif (len(img.shape) == 3):
        plot.imshow(cv2.cvtColor(norm_img, cv2.COLOR_BGR2RGB))
    plot.show()
    
    if file_name:
        cv2.imwrite(file_name, norm_img)

        
# Left : Source, Right : Target

def keypoints_to_coords(keypoints):
    """
    Converts keypoints into a numpy array of form [[x, y]]
    """
    return np.array([kp.pt for kp in keypoints])

def affine_left_matrix(coords):
    """
    Input: array of form [[x, y]]
    Returns a 2D array of form
    [   ...
        [x, y, 0, 0, 1, 0]
        [0, 0, x, y, 0, 1]
        ...
    ]
    """
    # Need to have 6 columns, and twice as many rows
    ret_dims = (coords.shape[0] * 2, 6)
    ret = np.empty(ret_dims, coords.dtype)
    
    # Use numpy indexing
    i = np.arange(coords.shape[0])
    
    # Even Rows: [x, y, 0, 0, 1, 0]
    ret[2*i, :2] = coords[i]
    ret[2*i, 2:] = [0, 0, 1, 0]
    
    # Odd Rows: [0, 0, x, y, 0, 1]
    ret[2*i + 1, :2] = [0, 0]
    ret[2*i + 1, 2:4] = coords[i]
    ret[2*i + 1, 4:] = [0, 1]
    
    return ret

def affine_right_matrix(coords):
    """
    Returns a 2D array of form 
    [
        [x]
        [y]
        ...
    ]
    """   
    # Return array needs to be twice as long
    ret = np.empty(coords.shape[0] * 2, dtype = coords.dtype)
    
    # Use numpy indexing
    i = np.arange(coords.shape[0])
    
    # Even Rows = x
    ret[2*i] = coords[i, 0]
    
    # Odd Rows = y 
    ret[2*i + 1] = coords[i, 1]
    
    return ret

def solve_affine_transform(left_kp_coords, right_kp_coords, k):
    
    assert k >= 3
    
    top_left, top_right = left_kp_coords[:k], right_kp_coords[:k]
    assert top_left.shape == top_right.shape
    
    # Using equation from lecture 8B: PA = P' -> A = P_inv * P'
    P = affine_left_matrix(top_left)
    P_prime = affine_right_matrix(top_right)
    
    # Compute inverse using moore-penrose pseudo inverse
    P_inv = np.linalg.pinv(P)
    
    # Approximation of affine transformation vector (a, b, c, d, e, f)
    (a, b, c, d, e, f) = np.matmul(P_inv, P_prime).flatten()
    
    # The affine transformation matrix
    return np.array(
        [[a, b, e],
         [c, d, f]]
    )

def affine_transform(coords, transform_matrix):
    """
    Computes the affine transform of coords (form [[x, y]]) with transform_matrix.
    """
    # Add ones onto the end of every row, then transpose the matrix (columns are [x, y, 1])
    num_pts, num_dims = coords.shape
    with_ones = np.ones((num_pts, num_dims + 1))
    with_ones[:, :-1] = coords
    with_ones = with_ones.transpose()
    
    # Array of form [[x...], [y...]]
    transformed = np.matmul(transform_matrix, with_ones)
    
    return transformed.transpose()

def draw_polygon(img, polygon_clockwise, color, thickness):
    """
    Draws the polygon whose corner points are specified in clockwise order 
    in polygon_clockwise (array of form [[x, y]]) 
    onto a copy of img.
    """
    ret = np.copy(img)
    
    num_corners = polygon_clockwise.shape[0]
    for i in range(num_corners):
        # Figure out which points to connect together
        left_ind,  right_ind = (i % num_corners), ((i + 1) % num_corners)
        left, right = polygon_clockwise[left_ind], polygon_clockwise[right_ind]
        
        # Draw a line between them (cv needs int tuples)
        left_tup, right_tup = tuple(left.astype(int)), tuple(right.astype(int))
        cv2.line(ret, left_tup, right_tup, color, thickness)
        
    return ret

def visualize_affine_transform(polygon_clockwise, img, transform_matrix):
    """
    Visualizes the affine transformation of transform_matrix by drawing a 
    quadrilateral (corner points specified by quadr, an array of form [[x, y]], clockwise order) 
    onto a copy of right_img.
    """
    # Transform the given polygon's corner points into new space
    new_poly = affine_transform(polygon_clockwise, transform_matrix)
    
    # Return the polygon drawn on the image
    return draw_polygon(img, new_poly, (0, 255, 0), 3)


def match_sift_descriptors(left, right):
    """
    Returns a 2D array of form [[i, j, distance]], where
        i - index of a vector in left
        j - index of the closest matching vector in right
        distance - integer distance between vectors i, j
    Results are sorted by the distance of the vector pairs.
    """   
    # [i, j]-th is euclidean distance between left[i], right[j]
    euc_dists = spatial.distance.cdist(left, right, 'euclidean')
    
    # [i, j]-th is the index of the j-th closest right-vector to left[i]
    sort_inds = np.argsort(euc_dists, axis=1)
    
    # top 2 matches are represented by first and second columns of above
    closest, closest2 = sort_inds[:, 0], sort_inds[:, 1]
    
    # Compute distance ratios between (left, first closest right) vs. (left, second closest left)
    left_inds = np.arange(left.shape[0])
    dist_ratios = euc_dists[left_inds, closest] / euc_dists[left_inds, closest2]
    
    # Suppress where distance ratio is above some threshold
    suppressed = dist_ratios * (dist_ratios < 0.8)

    # Get indices where suppression didn't happen
    left_inds = np.nonzero(suppressed)[0]
    right_inds = closest[left_inds]
    
    # Pair the above indices together, determine distance of pair
    pairs = np.stack((left_inds, right_inds)).transpose()
    pair_dists = euc_dists[pairs[:, 0], pairs[:, 1]]
    
    sorted_dist_inds = np.argsort(pair_dists)
    sorted_pairs = pairs[sorted_dist_inds]
    sorted_dists = pair_dists[sorted_dist_inds].reshape((sorted_pairs.shape[0], 1))
    
    return np.hstack((sorted_pairs, sorted_dists)).astype(int)


if __name__ == '__main__':

    imgname1 = '/Users/CYANG/Desktop/CSC420A3/reference.png'
    imgname2 = '/Users/CYANG/Desktop/CSC420A3/test.png'
    imgname3 = '/Users/CYANG/Desktop/CSC420A3/test2.png'

    sift = cv2.xfeatures2d.SIFT_create()

    img1 = cv2.imread(imgname1)
    kp1,desc1 = sift.detectAndCompute(img1,None)

    img2 = cv2.imread(imgname3)
    kp2,desc2 = sift.detectAndCompute(img2,None)

    matches = match_sift_descriptors(desc1, desc2)

    cover_kp_coords = keypoints_to_coords(kp1)[matches[:, 0]]
    find_cover_kp_coords = keypoints_to_coords(kp2)[matches[:, 1]]

    # Determine four corners of the book (clockwise order)
    cover_h, cover_w = img1.shape[:2]
    cover_quadr = np.array([
        [0, 0], [cover_w, 0],
        [cover_w, cover_h], [0, cover_h]
    ])

    k = 7
    print("Affine matrix and transform visualization using top {} matches:".format(k))
    
    matrix = solve_affine_transform(cover_kp_coords, find_cover_kp_coords, k)
    
    visualized = visualize_affine_transform(cover_quadr, img2, matrix)
    display_image(visualized, "q2d-output-top-k={}.jpg".format(k))




