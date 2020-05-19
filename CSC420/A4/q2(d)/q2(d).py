import numpy as np
from scipy import spatial, cluster
import scipy.io as spio
import cv2 as cv
import math
import re
import os
from collections import Counter
from matplotlib import pyplot as plot

def display_image(img, file_name=None, save_norm=True, save_type=np.uint8):
    """
    Shows an image (max-min normalized to 0-255), and saves it if a filename is given
    save_norm = whether to save the normalized image
    save_type = what datatype to save the image as
    """

    flt_img = img.astype(float)
    img_max, img_min = np.max(flt_img), np.min(flt_img)
    norm = (((flt_img - img_min) / (img_max - img_min)) * 255).astype(np.uint8)

    if len(img.shape) == 2:
        plot.imshow(norm, cmap='gray')
    elif (len(img.shape) == 3):
        plot.imshow(cv.cvtColor(norm, cv.COLOR_BGR2RGB))
    plot.show()

    to_save = norm if save_norm else flt_img
    if file_name:
        cv.imwrite(file_name, to_save)



if __name__ == '__main__':
   test_image_ids =[
    x.strip()
    for x in open("/Users/CYANG/Desktop/CSC420A4/data/test/test.txt", "r").readlines()
   ]

   CAR, PERSON, BICYCLE = 0, 1, 2
   cls_lst = [CAR, PERSON, BICYCLE]

   cls_to_name = {
        PERSON : "PERSON",
        BICYCLE : "BICYCLE",
        CAR : "CAR",
    }

   cls_to_col = {
        PERSON:(255, 0, 0), # Blue
        BICYCLE:(255, 255, 0),# Cyan
        CAR:(0, 0, 255), # Red
    }


   for img_id in test_image_ids[:3]:
       #{}.mat files #detactions =['__header__', '__version__', '__globals__', 'classes', 'dets','parts']
       detections = spio.loadmat("/Users/CYANG/Desktop/CSC420A4/data/test/results/dets-test/{}_dets".format(img_id))
       img = cv.imread("/Users/CYANG/Desktop/CSC420A4/data/test/left/{}.jpg".format(img_id))

       #car, person, bicycle, if its 1, then only has cars, if its 3, then it has all 3 objects
       num_class = detections['dets'].size
       #each image has 3 arrays, in each array there are list of objects
       #car class of each img: detections['dets'][0]
       #person class of each img: detections['dets'][1]
       #bicycle class of each img: detections['dets'][2]
       print(detections['dets'][0][0])

       class_lst = []
       for cls in range(num_class):#3
           object_lst = []
           for i in range(len(detections['dets'][cls][0])):#every object in each class
               obj = []

               for index in range(6):
                   obj.append(int(detections['dets'][cls][0][i][index]))

               object_lst.append(obj)
            
           class_lst.append(object_lst)
           print(class_lst)

       for i in range(num_class):
           for obj in class_lst[i]:
               cls = cls_lst[i]
               cv.rectangle(img, (obj[0], obj[1]), (obj[2], obj[3]),cls_to_col[cls] , 2)
               label_txt = cls_to_name[cls]
               label_coords = (obj[0], obj[1])
               cv.putText(img, label_txt, label_coords, cv.FONT_HERSHEY_SIMPLEX, 0.65, cls_to_col[cls], 2)

               #display_image(img, "q2c-{}-detections.png".format(img_id))


