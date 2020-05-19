import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy
import scipy.ndimage
import math

#Filter image with derivative of Gaussian (horizontal and vertical directions)
#Find magnitude and orientation of gradient
#Non-maximum suppression
#Linking and thresholding/hysteresis(NOT required)

def non_max_suppression(img, D):
        M, N = img.shape
        Z = np.zeros((M,N), dtype=np.int32)
        angle = D * 180. / np.pi
        angle[angle < 0] += 180

        for i in range(1,M-1):
            for j in range(1,N-1):
                try:
                    q = 255
                    r = 255

                   #angle 0
                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    #angle 45
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                    #angle 90
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                    #angle 135
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i,j] >= q) and (img[i,j] >= r):
                        Z[i,j] = img[i,j]
                    else:
                        Z[i,j] = 0

                except IndexError as e:
                    pass

        return Z

def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.uint8)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.uint8)

    Ix = ndimage.filters.convolve(img, Kx)
    Iy = ndimage.filters.convolve(img, Ky)

    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    return (G, theta)

def magnitude_of_gradients(img):

    img=cv2.imread(img,cv2.IMREAD_GRAYSCALE)

    # Define kernel for x differences
    kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]],np.float32)

    # Define kernel for y differences
    ky = np.array([[1,2,1],[0,0,0],[-1,-2,-1]],np.float32)

    #x convolution
    x = ndimage.convolve(img,ky, mode='constant', cval=0.0)

    #y convolution
    y = ndimage.convolve(img,kx, mode='constant', cval=0.0)

    #result = math.sqrt(x*x + y*y)
    result = np.hypot(x, y)
    result = result / result.max() * 255

    #convert type int32 to type unit8
    result2 = np.array(result,dtype=np.uint8)

    #get the orientation of the gradient
    theta = np.arctan2(y, x)
    
    #cv2.imshow('result',result2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return (result2,thera)

def canny_detect(img):
    #'/Users/CYANG/Desktop/waldo.png'
    img=cv2.imread(img,cv2.IMREAD_GRAYSCALE)

    #first smooth the original image
    smoothed = scipy.ndimage.filters.gaussian_filter(img,3)

    #using the function written in Q3(a) to get the magnitude
    #and orientation of the image
    gradient, theta = magnitude_of_gradients(smoothed)
    img2 = non_max_suppression(gradient, theta)

    #convert type int32 to type unit8
    result = np.array(img2,dtype=np.uint8)

    result = result[:,:,::-1]
    cv2.imshow('image', result)
    cv2.imwrite("testresult.png",result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result




