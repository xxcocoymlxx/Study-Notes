import numpy as np
import cv2
from scipy import ndimage

def create_gauss_filter(sigma):
    #length of the kernel is approx. 6*sigma round to odd
    if (6*sigma)%2 != 0:
        l = 6*sigma
    else:
        l = 6*sigma + 1
        
    #create the matrix
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    x, y = np.meshgrid(ax, ax)
    
    kernel = np.exp(-0.5 * (np.square(x) + np.square(y)) / np.square(sigma))

    return kernel / np.sum(kernel)

if __name__ == '__main__':
    img=cv2.imread('waldo.png',cv2.IMREAD_GRAYSCALE)
    gaussian_filter = create_gauss_filter(1)
    result = ndimage.convolve(img,gaussian_filter, mode='constant', cval=0.0)

    cv2.imshow('result image',result)
    cv2.waitKey(0)
