import cv2
import numpy as np
import matplotlib.pyplot as plt
import getopt
import sys
import random
import math
from scipy import spatial


#Runs through ransac algorithm, creating homographies from random correspondences
def ransac(corr, k, thresh):
    maxInliers = []
    finalH = None
    for i in range(k):
        #find 4 random points to calculate a homography
        corr1 = corr[random.randrange(0, len(corr))]
        corr2 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((corr1, corr2))
        corr3 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr3))
        corr4 = corr[random.randrange(0, len(corr))]
        randomFour = np.vstack((randomFour, corr4))

        #call the homography function on those points
        #h = calculateHomography(randomFour)
        h = calculateHomography(randomFour)
        inliers = []

        for i in range(len(corr)):
            d = geometricDistance(corr[i], h)
            if d < 5:
                inliers.append(corr[i])

        if len(inliers) > len(maxInliers):
            maxInliers = inliers
            finalH = h

        if len(maxInliers) > (len(corr)*thresh):
            break
    return finalH, maxInliers



#Calculate the geometric distance between estimated points and original points
def geometricDistance(correspondence, h):

    p1 = np.transpose(np.matrix([correspondence[0].item(0), correspondence[0].item(1), 1]))
    estimatep2 = np.dot(h, p1)
    estimatep2 = (1/estimatep2.item(2))*estimatep2

    p2 = np.transpose(np.matrix([correspondence[0].item(2), correspondence[0].item(3), 1]))
    error = p2 - estimatep2
    return np.linalg.norm(error)


def match_sift_descriptors(left, right):
    """
    Returns a 2D array of form [[i, j, distance]], where
        i - index of a vector in left
        j - index of the closest matching vector in right
        distance - integer distance between vectors i, j
    Results are sorted by the distance of the vector pairs.
    """
    # Return empty if either left or right is empty
    left_empty = (left is None) or (len(left) == 0)
    right_empty = (right is None) or (len(right) == 0)
    if left_empty or right_empty:
        return np.empty((0, 3)).astype(int)
    
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


# Computers a homography from 4-correspondences
def calculateHomography(correspondences):
    #loop through correspondences and create assemble matrix
    aList = []
    for corr in correspondences:
        p1 = np.matrix([corr.item(0), corr.item(1), 1])
        p2 = np.matrix([corr.item(2), corr.item(3), 1])

        a2 = [0, 0, 0, -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
              p2.item(1) * p1.item(0), p2.item(1) * p1.item(1), p2.item(1) * p1.item(2)]
        a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2), 0, 0, 0,
              p2.item(0) * p1.item(0), p2.item(0) * p1.item(1), p2.item(0) * p1.item(2)]
        aList.append(a1)
        aList.append(a2)

    matrixA = np.matrix(aList)

    #svd composition
    u, s, v = np.linalg.svd(matrixA)

    #reshape the min singular value into a 3 by 3 matrix
    h = np.reshape(v[8], (3, 3))

    #normalize and now we have h
    h = (1/h.item(8)) * h
    return h


if __name__ == '__main__':

    imgname1 = '/Users/CYANG/Desktop/CSC420A3/landscape_1.jpg'
    imgname2 = '/Users/CYANG/Desktop/CSC420A3/landscape_2.jpg'

    img1 = cv2.imread(imgname2)
    img2 = cv2.imread(imgname1)

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    estimation_thresh = 0.8

    correspondenceList = []
    if img1 is not None and img2 is not None:
        kp1, desc1 = sift.detectAndCompute(img1,None)
        kp2, desc2 = sift.detectAndCompute(img2,None)

        matches = match_sift_descriptors(desc1, desc2)

        for match in matches:
            (x1, y1) = kp1[match[0]].pt
            (x2, y2) = kp2[match[1]].pt
            correspondenceList.append([x1, y1, x2, y2])

        corrs = np.matrix(correspondenceList)

        finalH, inliers = ransac(corrs, 1000,estimation_thresh)
        dst = cv2.warpPerspective(img1,finalH,(img2.shape[1] + img1.shape[1], img2.shape[0]))
        dst[0:img2.shape[0], 0:img2.shape[1]] = img2

        result = dst[:,:,::-1]
        cv2.imshow('wooooooooowwwwww',result)
        cv2.waitKey(0)
