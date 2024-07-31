import cv2
import numpy as np
import os
import glob
from similar import runAllImageSimilaryFun

for file in glob.glob(os.path.join("image-find","*.png")):
    print(file)
    img = cv2.imread(file)
    y,x,_ = img.shape
    img = img[int(475/1440*y):int(546/1440*y), int(1057/2560*x):int(1459/2560*x)]
    cv2.resize(img, dsize=(71, 402))
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, lowerb=np.array([200,240,240]), upperb=np.array([360,255,255]))
    img = cv2.bitwise_and(img,img,mask=mask)
    cv2.imwrite("imgs\\test-find-temp.png",img)
    runAllImageSimilaryFun("imgs\\test-find.png","imgs\\test-find-temp.png")
    #os.system("pause")