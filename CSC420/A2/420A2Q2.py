from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import math

def BiLinear_interpolation(img):
    img = np.array(Image.open(img))
    scrH,scrW,_ = img.shape
    #upscales an image to a 3x resolution
    dstH = scrH*3
    dstW = scrW*3
    img=np.pad(img,((0,1),(0,1),(0,0)),'constant')
    retimg=np.zeros((dstH,dstW,3),dtype=np.uint8)
    
    for i in range(dstH):
        for j in range(dstW):
            scrx=(i+1)*(scrH/dstH)-1
            scry=(j+1)*(scrW/dstW)-1
            x=math.floor(scrx)
            y=math.floor(scry)
            u=scrx-x
            v=scry-y
            retimg[i,j]=(1-u)*(1-v)*img[x,y] + u*(1-v)*img[x+1,y] + (1-u)*v*img[x,y+1] + u*v*img[x+1,y+1]

    result = Image.fromarray(retimg.astype('uint8')).convert('RGB')
    result.save("/Users/CYANG/Desktop/test_result.png")
    return result
