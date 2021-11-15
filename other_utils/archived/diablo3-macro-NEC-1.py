import pyautogui
from threading import Thread
from time import sleep
from os import system
from traceback import format_exc

'''
DESC

NAME = D3 NEC S22速刷辅助按键脚本
AUTHOR = CERES
DATE = 2020-12-26
VER = 1.0

游戏内技能设置：

    依次为1，2，3，4，鼠左，鼠右

    衰老，吞噬/吞噬灵气，血步，分身；骨矛，骨甲

思路：

    1.5秒间隔释放1技能，1秒间隔2技能

    点指敌人释放左键技能，点指地面移动

    点指物品拾取。其它技能手动。


'''

class Macro(object):
    def __init__(self):
        # add the acts you wanted to do here:
        self.acts = [
            self.mouse1,
            self.s1,
            # self.s2,
            self.potion
        ]

    def mouse1(self):
        pyautogui.click(clicks=100000, interval=0.1, button='left')

    def s1(self):
        pyautogui.press("1", presses=100000, interval=1.45)

    def s2(self):
        pyautogui.press("2", presses=100000, interval=1)

    def potion(self):
        pyautogui.press("q", presses=100000, interval=0.3)

    def start(self):
        sleep(1.5)
        pyautogui.press("4")

        for a in self.acts:
            x = Thread(target=a)
            x.start()


if __name__ == "__main__":
    try:
        m = Macro()
        m.start()
    except Exception:
        pyautogui.click(button="right")
        print(format_exc())
        system("pause")
