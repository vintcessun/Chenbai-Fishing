import os
import glob
import cv2
from imgchange import cut

number_tag={1:"none",
2:"normal",
3:"perfect"
}

files = {}
filelist = glob.glob(os.path.join("image-4", "*.png"))

for file in filelist:
    num = int(file.split("\\")[-1].split("-")[0])
    files[num] = file;

keys = list(files.keys())
keys.sort()

t=0
num = 91;
for i in keys:
    file = files[i]
    filename = file.split("\\")[-1]
    img = cv2.imread(file)
    y,x,_ = img.shape
    _img = cut(img,x,y)
    cv2.imshow('image', _img)
    k = cv2.waitKey(0)
    tag = int(k)-int(ord('0'))
    if tag>=1 and tag<=3:
        target = number_tag[tag];
        print(f"标签为 {target}")
        outer = f"test\\{target}\\{filename}"
        cv2.imwrite(outer, img)
        print(f"保存到 {outer}")
        os.system(f'del "{file}"')
        print(f"已删除 {file}")
    elif tag==4:
        del_num=int(now_cb.split("-")[0])
        print(f"删除{del_num}-4.png到{del_num+num-1}-4.png")
        for i in range(num):
            os.system(f"del image-4\\{del_num+i}-4.png")
    elif tag==5:
        os.system(f'del "{file}"')
        print(f"已删除 {file}")
    else:
        raise;
    t=t+1
    print(f"已完成{t}/{len(keys)}")
    print(f"进度 {100*t/len(keys)}%")