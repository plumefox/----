import ctypes
import os
import random
import sys
import time


keystrokes = 0
mouse_clicks = 0
double_clicks = 0

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('dwTime', ctypes.c_ulong)
    ]

def get_last_input ():
    """获取距离上次输入事件的时间

    Returns:
        time: 距离上次输入事件的时间
    """
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
    
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))
    
    #获得机器运行的时间
    runtime = ctypes.windll.kernel32.GetTickCount()
    elapsed = runtime - struct_lastinputinfo.dwTime

    print(f"[*] It's been {elapsed} milliseconds since the last input event.")
    return elapsed

def get_key_press():
    global mouse_clicks
    global keystrokes
    for i in range(0,0xff):
        state = ctypes.windll.user32.GetAsyncKeyState(i)
        if (state & 0x0001):
            #鼠标左键按下
            if (i == 0x1):
                mouse_clicks +=1
                return time.time()
            #键盘上ascii
            elif (i>32 and i<127):
                keystrokes+=1
    return None

def detect_sandbox():
    global mouse_clicks
    global keystrokes
    
    max_keystrokes = random.randint(10,25)
    max_mouse_clicks = random.randint(5,25)
    double_clicks = 0 #双击
    max_double_clicks = 10 #最大双击
    double_clicks_threshold = 0.25 #秒 定义双击间隔
    first_double_click = None #第一次双击
    average_mousetime = 0 #平均点击间隔
    max_input_threshold = 30000 #毫秒 最大无动作时间
    previous_timestamp = None
    detection_complete = False
    
    last_input = get_last_input()
    
    if (last_input > max_input_threshold):
        sys.exit(0)
    
    # 上一次点击没超过
    print("lastinput over")
    while not detection_complete:
        # print(f"mouseclick = {mouse_clicks}, keystrokes = {keystrokes},doubleclicks = {double_clicks}")
        # 获取鼠标点击时间
        keypress_time = get_key_press()
        
        if (keypress_time is not None and previous_timestamp is not None):
            # 两次点击间隔
            elapsed = keypress_time - previous_timestamp
            
            # 认为是双击
            if(elapsed <= double_clicks_threshold):
                # print(f"双击 {double_clicks}")
                double_clicks+=1
                # 第一次双击
                if (first_double_click is None):
                    first_double_click = time.time()
                else:
                    #双击次数达到上限
                    if double_clicks == max_double_clicks:
                        print(f"达到最大双击次数")
                        # 上一次双击-第一次双击 <= 连续点击最大花费的时间 ->处于连续点击
                        print(f"目前:{keypress_time - first_double_click} 最大:{max_double_clicks * double_clicks_threshold}")
                        if (keypress_time - first_double_click<= 
                            (max_double_clicks * double_clicks_threshold)):
                            print(f"短时间连续双击 触发退出")
                            sys.exit(0)
            # 达到检测数量 全部通过
            if(keystrokes >= max_keystrokes and 
                double_clicks >= max_double_clicks and 
                mouse_clicks>=max_mouse_clicks):
                return
            previous_timestamp = keypress_time
        elif(keypress_time is not None):
            previous_timestamp = keypress_time

if __name__ == '__main__':
    
    if os.name == "nt":
        detect_sandbox()
        print("we are ok")
        
        
    
    

