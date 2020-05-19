import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randrange


if __name__ == '__main__':

    imgname1 = '/Users/CYANG/Desktop/CSC420A3/landscape_1.jpg'
    imgname2 = '/Users/CYANG/Desktop/CSC420A3/landscape_2.jpg'

    img_ = cv2.imread(imgname2)
    img1 = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)
    img = cv2.imread(imgname1)
    img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m in matches:
        if m[0].distance < 0.5*m[1].distance:
            good.append(m)
            matches = np.asarray(good)

    if len(matches[:,0]) >= 4:
        src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
        dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
        H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 2.0)
    else:
        raise AssertionError("Can’t find enough keypoints.")

    dst = cv2.warpPerspective(img_,H,(img.shape[1] + img_.shape[1], img.shape[0]))
    dst[0:img.shape[0], 0:img.shape[1]] = img
    #cv2.imwrite('StitchingOutput.jpg',dst)

    
    result = dst[:,:,::-1]
    cv2.imshow('sp',result)
    cv2.waitKey(0)
