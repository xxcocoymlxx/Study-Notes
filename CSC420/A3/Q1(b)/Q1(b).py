import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from skimage import data
from PIL import Image
from scipy import spatial

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


def draw_keypoints(img1,kp1,img2,kp2,matches):
    '''
    kp1 is of type 'KeyPoint' and it contains attibutes like
    coordinates and scale of a key point.

    matches are list of list of the form [[i, j, distance]], where
        i - index of a vector in left
        j - index of the closest matching vector in right
    '''
    #for img1
    fig,ax = plt.subplots(1)
    ax.imshow(img1)

    color_list = ['r','g','b']
    for i in range(3):
        rect = patches.Rectangle(kp1[matches[i][0]].pt,(kp1[matches[i][0]].size)*10,(kp1[matches[i][0]].size)*10,linewidth=2,edgecolor=color_list[i],facecolor='none')
        ax.add_patch(rect)
    plt.show()

    #for img2
    fig,ax = plt.subplots(1)
    ax.imshow(img2)
    for i in range(3):
        rect = patches.Rectangle(kp2[matches[i][1]].pt,(kp2[matches[i][1]].size)*10,(kp2[matches[i][1]].size)*10,linewidth=2,edgecolor=color_list[i],facecolor='none')
        ax.add_patch(rect)

    plt.show()
    
    
if __name__ == '__main__':

    imgname1 = '/Users/CYANG/Desktop/CSC420A3/reference.png'
    imgname2 = '/Users/CYANG/Desktop/CSC420A3/test.png'
    imgname3 = '/Users/CYANG/Desktop/CSC420A3/test2.png'

    sift = cv2.xfeatures2d.SIFT_create()

    img1 = np.array(Image.open(imgname1), dtype=np.uint8)
    kp1,desc1 = sift.detectAndCompute(img1,None)

    img2 = np.array(Image.open(imgname3), dtype=np.uint8)
    kp2,desc2 = sift.detectAndCompute(img2,None)

    matches = match_sift_descriptors(desc1, desc2)

    draw_keypoints(img1,kp1,img2,kp2,matches)

