import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
import os
from random import random, randint


'''
auto click, simple

'''


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.name = "快速左击宏"
        self.counter = 0

    def watcher(self):
        # 守护者，用于设置全局宏开关标志位，该函数需要在主进程中调用
        print(self.name)
        while True:
            if keyboard.is_pressed('ctrl'):
                self.autoClick(100) # 快速点击1000次

            pyautogui.sleep(0.1)

    def autoClick(self, repeats):
        self.counter += 1
        pyautogui.click(clicks=repeats,button='left', _pause=True)

if __name__ == "__main__":
    try:
        m = Macro()
        m.watcher()
    except Exception as e:
        print(format_exc())
