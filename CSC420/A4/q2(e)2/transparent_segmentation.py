import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy.io
import matplotlib.colors as mcolors
import webcolors

if __name__ == '__main__':
    base_path = "/Users/CYANG/Desktop/A4/q2(e)2/"

    test_image_ids =[
    x.strip()
    for x in open(base_path+"test.txt", "r").readlines()
    ]

    for img_id in test_image_ids[:3]:
        
        gt_mask = cv2.imread(base_path+'q2e-{}-segmentation.png'.format(img_id),cv2.IMREAD_GRAYSCALE)
        plt.imshow(gt_mask)
        plt.show()
        gt_mask.shape
        print(gt_mask.max())
        print(gt_mask.min())
        # 16 is background
        obj_ids = np.unique(gt_mask)
        print(obj_ids)
        number_object = obj_ids.shape[0]

        # norm ids
        count = 0
        for o_id in obj_ids:
            gt_mask[gt_mask == o_id] = count
            count += 1

        base_COLORS = []

        for key, value in mcolors.CSS4_COLORS.items():
            rgb = webcolors.hex_to_rgb(value)
            base_COLORS.append([rgb.blue, rgb.green, rgb.red])
        base_COLORS = np.array(base_COLORS)

        np.random.seed(99)
        base_COLORS = np.random.permutation(base_COLORS)

        colour_id = np.array([(id) % len(base_COLORS) for id in range(number_object)])

        COLORS = base_COLORS[colour_id]
        COLORS = np.vstack([[0, 0, 0], COLORS]).astype("uint8")
        mask = COLORS[gt_mask]

        imgLeft = cv2.imread(base_path+'left/{}.jpg'.format(img_id))
        output = ((0.4 * imgLeft) + (0.6 * mask)).astype("uint8")
        plt.imshow(output[:,:,::-1])
        plt.show()

