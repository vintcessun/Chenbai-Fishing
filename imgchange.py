import cv2
import numpy as np
import os
import glob

def change(img):
    mask_normal_and_tag = cv2.inRange(img, lowerb=np.array([230,225,225]), upperb=np.array([270,255,255]))
    mask_perfect = cv2.inRange(img, lowerb=np.array([0,180,180]),upperb=np.array([40,255,255]))
    mask = cv2.bitwise_or(mask_normal_and_tag,mask_perfect)
    ret = cv2.bitwise_and(img,img,mask=mask)
    return ret

#裁切为(1520,314)->(1994,788)的474*474图形
#源图为2560x1440这里用比例来弄
#1920x1080=>(1140,235)->(1542,591)
def cut(img,x,y):
    #print(img.shape)
    cropped = img[int(314/1440*y):int(788/1440*y), int(1520/2560*x):int(1994/2560*x)]  # 裁剪坐标为[y0:y1, x0:x1]
    return cropped

def imgreshape(img):
    ret = cv2.resize(img, dsize=(256, 256))
    return ret;

def all_change(img):
    #x,y = 2560, 1440;#自行更改为分辨率
    y,x,_ = img.shape
    img = cut(img, x, y)
    img = change(img)
    img = imgreshape(img)
    return img

def main():
    x,y = 2560, 1440;#自行更改为分辨率
    
    for tag in os.listdir("test"):
        for file in glob.glob(os.path.join("test", tag, "*.png")):
            outer = file.replace("test","data")
            print(f'"{file}"=>"{outer}"')
            img = cv2.imread(file)
            img = all_change(img)
            cv2.imwrite(outer,img)
            os.system(f'del "{file}"')

def test():
    img = cv2.imread("imgs\\test-source.png")
    img = all_change(img)
    cv2.imwrite("imgs\\test.png",img)

if __name__=='__main__':
    main()