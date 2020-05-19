import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
import math

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

