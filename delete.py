import os;
import pandas.io.clipboard as cb
import time;

num = 91;
last_cb = cb.paste()
while(1):
    now_cb=cb.paste()
    if(now_cb!=last_cb):
        print(f"发现剪切板更改为{now_cb}")
        try:
            t=int(now_cb.split("-")[0])
            print(f"删除{t}-4.png到{t+num-1}-4.png")
            for i in range(num):
                os.system(f"del image-4\\{t+i}-4.png")
        except:
            pass
    time.sleep(0.5)
    last_cb=now_cb