print("请等待预加载，可能因为设备性能而有差异")

from keras.models import load_model
import cv2
import numpy as np
import pyautogui
from pyautogui import press
import time
import os
import win32gui,win32ui,win32con

from imgchange import all_change

window = False
number_tag={0:"none",
1:"normal",
2:"perfect"
}

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
load_model = load_model(get_path("model"))
pyautogui.FAILSAFE = False
find1 = cv2.imread(get_path("imgs/test-find-1.png"))
find2 = cv2.imread(get_path("imgs/test-find-2.png"))
success = cv2.imread(get_path("imgs/test-success.png"))
pre = cv2.imread(get_path("imgs/test-pre.png"))
hwnd = 0
screenshot = None
print("预加载完成")

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
 
    return os.path.normpath(os.path.join(base_path, relative_path))

def Template(source,template,pos=[0,0]):
    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.95)#我截得图小，0.95效果好
    y,x=loc
    ret=[]
    for i in range(len(y)):
        if(i==0):
            ret.append((x[i]+pos[0],y[i]+pos[1]))
        elif(abs(x[i]-x[i-1])>10 or abs(y[i]-y[i-1])>10):
            ret.append((x[i]+pos[0],y[i]+pos[1]))
    return ret;

def screenshot_all():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)

def screenshot_window():
    title = cv2.imread(get_path("imgs/test-title.png"))
    img = screenshot_all()
    x,y = Template(img,title)[0]
    x = x-40
    y = y+33
    width = 1080
    height = 1920
    def inner():
        img = screenshot_all()
        img = img[y:(y+width), x:(x+height)]
        return img
    return inner

if window:
    print("将在5s后匹配窗口，请点击窗口")
    time.sleep(5)
    screenshot=screenshot_window()
    print("匹配完成")
else:
    screenshot=screen_shot_all


def get_result(predicted):
    predicted = list(predicted)
    return predicted.index(max(predicted))

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    if(type(degree)==np.ndarray):
        return degree[0]
    else:
        return degree



def similar_find(image):
    y,x,_ = image.shape
    img = image[int(475/1440*y):int(546/1440*y), int(1057/2560*x):int(1459/2560*x)]
    img = cv2.resize(img, dsize=(402, 71))
    mask = cv2.inRange(img, lowerb=np.array([200,240,240]), upperb=np.array([360,255,255]))
    img = cv2.bitwise_and(img,img,mask=mask)
    degree = calculate(img, find1)
    if degree>0.9:
        return True;
    else:
        img = image[int(326/1440*y):int(363/1440*y), int(1169/2560*x):int(1369/2560*x)]
        img = cv2.resize(img, dsize=(300, 37))
        mask = cv2.inRange(img, lowerb=np.array([200,200,200]), upperb=np.array([360,255,255]))
        img = cv2.bitwise_and(img,img,mask=mask)
        degree = calculate(img, find2)
        #print(degree)
        if degree>0.9:
            return True
        else:
            return False

def similar_success(image):
    y,x,_ = image.shape
    img = image[int(417/1440*y):int(483/1440*y), int(1142/2560*x):int(1417/2560*x)]
    img = cv2.resize(img, dsize=(275, 66))
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lowerb=np.array([0,0,221]), upperb=np.array([180,30,255]))
    img = cv2.bitwise_and(img,img,mask=mask)
    degree = calculate(img,success)
    #print(degree)
    return degree>0.9

def similar_window(image):
    y,x,_ = image.shape
    img = image[int(1136/1440*y):int(1422/1440*y), int(2223/2560*x):int(2509/2560*x)]
    img = cv2.resize(img, dsize=(286, 286))
    mask = cv2.inRange(img, lowerb=np.array([150,180,200]), upperb=np.array([180,200,255]))
    img = cv2.bitwise_and(img,img,mask=mask)
    img = img[101:179,101:179]
    degree = calculate(img,pre)
    #print(degree)
    return degree>0.95

def action():
    date = False;#True 开始钓鱼识别 False关闭
    can_finish = False;
    print("开始侦测屏幕")
    while(1):
        image = screenshot()
        if not date:
            if similar_find(image):
                press(" ")
                print("找到鱼")
                date = True
                print("正在自动钓鱼")
                time.sleep(0.25)
                continue
        if date and can_finish:
            if similar_success(image):
                print("结算页面")
                t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
                file = f"result\\{t}.png"
                cv2.imwrite(file, image)
                print(f"已保存到{file}")
                date=False
                press("esc")
                break
        if date:
            img = all_change(image)
            img = img.reshape(256,256,3) / 255.0
            img = np.asarray([img], np.float32)
            predicted = load_model.predict(img,verbose=0)[0]
            predicted = get_result(predicted)
            if(predicted == 2):
                press(" ")
                print(f"识别到perfect")
                can_finish = True
                time.sleep(1.6)

def main():
    while(1):
        img = screenshot()
        if similar_window(img):
            print("发现钓鱼界面")
            press(" ")
            action()

def test():
    print("正在测试模型可用性")
    unknown_none = cv2.imread(get_path('imgs/none.png')).reshape(256,256,3) / 255.0
    unknown_normal = cv2.imread(get_path('imgs/normal.png')).reshape(256,256,3) / 255.0
    unknown_perfect = cv2.imread(get_path('imgs/perfect.png')).reshape(256,256,3) / 255.0
    unknown = np.asarray([unknown_none,unknown_normal,unknown_perfect], np.float32)
    predicted = load_model.predict(unknown,verbose=0)
    if get_result(predicted[0]) == 0 and get_result(predicted[1]) == 1 and get_result(predicted[2]) == 2:
        print("模型可用")
        return True;
    else:
        return False;

if __name__=="__main__":
    if(test()):
        main()