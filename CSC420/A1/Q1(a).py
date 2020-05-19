import numpy
import cv2
import matplotlib.pyplot as plt

def calculate(padded_img, filter, i, j):
	f_h, f_w = filter.shape
	summed = 0
	for k in range(f_h):
		n_j = j
		for l in range(f_w):
			summed = summed + (filter[k][l] * padded_img[i][n_j])
			n_j = n_j + 1
		i = i + 1
	return summed


def convolution(image, filter):  
	# get size of the filter
	filter_size = filter.shape[1]

	#the image we passed in is already grey
	#get dimensions of the ORIGINAL image
	img_height, img_width = image.shape

	#we assume we will have a filter of odd size
	#and it’s a square matrix
	size_pad = filter_size - 1

	# create a empty matrix filled with zero
	ni_h = img_height + size_pad
	ni_w = img_width + size_pad
	new_img = numpy.zeros((ni_h, ni_w), 'uint8')

	# copy image into matrix
	new_img[(size_pad//2):(ni_h-(size_pad//2)), (size_pad//2):(ni_w-(size_pad//2))] = image

	# flip the filter
	flipped_filter = filter[::-1,::-1]

	#a new image container
	img_copy = image.copy()

	# get the convoved value of each pixel
        #remember here we are using the size of the ORIGINAL image
        #because we want the size to be the same
	for i in range(img_height):
		for j in range(img_width):
                        #we use the padded image to calculate the convolution
                        #to deal with the edge
			img_copy[i][j] = calculate(new_img, flipped_filter, i, j)

	return img_copy
	

if __name__ == '__main__':
    f = numpy.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
    #Load an color image in grayscale
    img=cv2.imread('waldo.png',cv2.IMREAD_GRAYSCALE)
    result = convolution(img, f)
    cv2.imshow('result image',result)
    cv2.waitKey(0)

