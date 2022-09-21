import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
'''
D3 自动分解与血岩赌博 脚本

思路：

    1. F5 触发自动分解

            注意：为了防止误触，按F5+F6！

        [TODO]

            设置安全区域
        
    2.  F9 触发自动赌博

'''


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.name = "D3 自动分解与血岩赌博 脚本"

    def watcher(self):
        # 守护者，用于设置全局宏开关标志位，该函数需要在主进程中调用
        print(self.name)
        while True:
            if keyboard.is_pressed('f5'):
                if keyboard.is_pressed('f6'):
                    self.abort = False
                    self.autoDecom()
            if keyboard.is_pressed('f9'):
                self.abort = False
                self.autoBet()

            pyautogui.sleep(0.1)

    def autoDecom(self):
        # 自动分解
        pyautogui.click(x=520, y=480, button='left', _pause=False)  # 调出分解界面
        pyautogui.sleep(0.1)
        pyautogui.click(x=160, y=300, button='left', _pause=False)  # 点击分解按钮
        lines = (0, 2, 4, 1, 3, 5)
        for i in lines:
            for j in range(10):
                if not keyboard.is_pressed('esc'):
                    pyautogui.click(x=1427+50*j, y=584+50*i, button='left', _pause=False)
                    # pyautogui.sleep(0.03)
                    pyautogui.press('enter', _pause=False)
                    # pyautogui.sleep(0.04)
                else:
                    break

    def autoBet(self):
        if self.abort == False:
            pyautogui.click(clicks=30, button='right',
                            interval=0.0, _pause=False)


if __name__ == "__main__":
    try:
        m = Macro()
        m.watcher()
    except Exception as e:
        print(format_exc())
