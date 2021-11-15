import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
'''
D3圣教军散件荆棘炮轰应该是最“抠脚”的BD了（当然前提是需要宏的配合）。

思路：

    所有技能，CD完毕立即使用即可。

    左键为主动炮轰，点到敌人即为技能，点到地面即为移动，点到物品即为拾取。

'''

class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.stop = True

        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"

        self.acts = [
            self.forceMove,
            self.mouse1,
            self.mouse2,
            self.s1,
            self.s2,
            self.s3,
            self.s4,
            self.potion
        ]

    def watcher(self):
        # 守护者，用于设置全局宏开关标志位，该函数需要在主进程中调用
        tmp = self.stop
        while True:
            # print(self.stop)
            if keyboard.is_pressed(self.globalSwitchOn):
                self.stop = False
            if keyboard.is_pressed(self.globalSwitchOff):
                self.stop = True
            pyautogui.sleep(0.1)
            if self.stop != tmp:
                tmp = self.stop
                print(f'stop={tmp}')

    def forceMove(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("`")
                pyautogui.sleep(1)
                pyautogui.keyUp('`')
            pyautogui.sleep(0.2)

    def mouse1(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='left')
            pyautogui.sleep(0.1)

    def mouse2(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='right')
            pyautogui.sleep(0.1)

    def s1(self):
        while True:
            if self.stop == False:
                pyautogui.press("1")
            pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.press("2")
            pyautogui.sleep(0.1)

    def s3(self):
        while True:
            if self.stop == False:
                pyautogui.press("3")
            pyautogui.sleep(0.1)

    def s4(self):
        while True:
            if self.stop == False:
                pyautogui.press("4")
            pyautogui.sleep(0.1)

    def potion(self):
        while True:
            if self.stop == False:
                pyautogui.press("q")
            pyautogui.sleep(0.1)

    def start(self):
        for a in self.acts:
            x = Thread(target=a)
            x.start()


if __name__ == "__main__":
    try:
        m = Macro()
        m.start()
        print('watching...')
        m.watcher()

    except Exception as e:
        pyautogui.click(button="right")
        pyautogui.press("`")
        print(format_exc())
