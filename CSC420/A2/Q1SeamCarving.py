import scipy
from PIL import Image
import numpy as np
from pylab import *
from scipy import ndimage
import scipy.misc as sm
from PIL import Image
import cv2

#Q1 Seam Carving
'''
The optimal seam can be found using dynamic programming. The
1. first step is to traverse the image from the second row to the last row
and compute the cumulative minimum energy M for all possible
connected seams for each entry (i, j):
M(i, j) = e(i, j) + min(M(i−1, j −1),M(i−1, j),M(i−1, j +1))

2. At the end of this process, the minimum value of the last row in
M will indicate the end of the minimal connected vertical seam. Hence, backtrack from this minimum entry on
M to find the path of the optimal seam
'''

#Step 1 calculate image gradient (energy) of given image
def get_energy_function(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    Gr = magnitude_of_gradients(R)
    Gg = magnitude_of_gradients(G)
    Gb = magnitude_of_gradients(B)

    #TA said simply add them together
    img_gradient = Gr + Gg + Gb

    #sm.imshow(img_gradient)

    return img_gradient

def magnitude_of_gradients(img):

    # Define kernel for x and y differences
    kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]],np.float32)
    ky = np.array([[1,2,1],[0,0,0],[-1,-2,-1]],np.float32)

    x = ndimage.convolve(img,ky, mode='constant', cval=0.0)
    y = ndimage.convolve(img,kx, mode='constant', cval=0.0)

    #result = math.sqrt(x*x + y*y)
    result = np.hypot(x, y)
    result = result / result.max() * 255

    #convert type int32 to type unit8
    result2 = np.array(result,dtype=np.uint8)

    #cv2.imshow('result',result2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return result2


#Step 2: build a map of the minimum cumulative energies
def cumulative_energy(energy):
    """
    energy: 2D numpy.array, image gradient
    Returns:
        tuple of 2 2D numpy.array
        paths: x-offset of the previous seam element for each pixel.
        cumulative_energies: cumulative energy at each pixel.
        seam_tail: the x-coordinate of the pixel in the last row
        of cumulative_energies with least energy.
    """
    height, width = energy.shape

    #pad with zeros first
    paths = np.zeros((height, width), dtype=np.int64)
    cumulative_energies = np.zeros((height, width), dtype=np.int64)
    paths[0] = np.arange(width) * np.nan

    for i in range(1, height):
        for j in range(width):
            #M(i, j) = e(i, j) + min(M(i−1, j −1),M(i−1, j),M(i−1, j +1))
            prev_energies = cumulative_energies[i-1, max(j-1, 0):j+2]
            least_energy = prev_energies.min()
            cumulative_energies[i][j] = energy[i][j] + least_energy
            paths[i][j] = np.where(prev_energies == least_energy)[0][0] - (1*(j != 0))

    #get the x-coordinate of the pixel with least energy
    seam_tail = list(cumulative_energies[-1]).index(min(cumulative_energies[-1]))

    return paths, cumulative_energies, seam_tail


#Step 3: do a backtrace to get the path (“seam”) with the lowest energy
def find_seam(paths, end_x):
    """
    paths: 2D numpy.array. Each element of the matrix is the offset
    of the index to the previous pixel in the seam
    end_x: integer. The x-coordinate of the pixel with the min energy in the last row 
    Returns a 1D numpy.array with length == height of the image
    Each element is the x-coordinate of the pixel to be removed at that y-coordinate. e.g.
    [4,4,3,2] means "remove pixels (0,4), (1,4), (2,3), and (3,2)"
    """
    height, width = paths.shape[:2]
    seam = [end_x]
    for i in range(height-1, 0, -1):
        cur_x = seam[-1]
        offset_of_prev_x = paths[i][cur_x]
        seam.append(cur_x + offset_of_prev_x)
    seam.reverse()
    return seam


#Step 4: delete the pixels which belong to the seam
def remove_seam(img, seam):
     """
    img: 3D numpy.array RGB image
    seam: 1D numpy.array seam to remove
    Returns 3D numpy array of the image with the seam removed
    """
 #    img = np.array(Image.open(img))
     height, width, _ = img.shape
     return np.array([np.delete(img[row], seam[row], axis=0) for row in range(height)])


if __name__ == "__main__":

    img = "/Users/CYANG/Desktop/fall.jpg"
    image = np.array(Image.open(img))
    
    for i in range (100):
        #Step 1: calculate the energy for each pixel of the image
        energy_map = get_energy_function(image)
        paths, cumulative_energies, seam_tail = cumulative_energy(energy_map)

        #Step 2: build a map of the minimum cumulative energies
        paths, cumulative_energies, seam_tail = cumulative_energy(energy_map)

        #Step 3: do a backtrace on this data to get the path (“seam”) with the lowest energy
        seam = find_seam(paths, seam_tail)

        #Step 4: delete the pixels which belong to the seam
        image = remove_seam(image, seam)
        

    image = image[:,:,::-1]
    
    cv2.imshow('result',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

