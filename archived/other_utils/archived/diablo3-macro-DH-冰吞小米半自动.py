import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
'''
D3 DH 冰吞小密境 半自动 脚本

思路：

    右键扫射不加入宏序列，长按攻击赶路，拣东西或过门时可以酌情松开鼠标右键长按。


'''


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.stop = True
        self.counter = 0

        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"
        self.globalSwitchPause = "ctrl"
        self.firstRun = True

        self.acts = [
            # self.forceMove,
            self.mouse1,
            # self.mouse2,
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
                self.counter = self.counter + 1
            if keyboard.is_pressed(self.globalSwitchOff):
                self.stop = True
                self.firstRun = True
            if keyboard.is_pressed(self.globalSwitchPause):
                self.stop = True
            pyautogui.sleep(0.1)
            if self.stop != tmp:
                tmp = self.stop
                print(f'counter={self.counter},stop={tmp}')

    def forceMove(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("`")
                pyautogui.sleep(1)
                pyautogui.keyUp('`')
            else:
                pyautogui.sleep(0.2)

    def ent(self):
        # 进场动作
        for i in range(7):
            pyautogui.keyDown("2")
            pyautogui.sleep(0.05)
            pyautogui.keyUp("2")

    def mouse1(self):
        while True:
            # 宠物，拣物
            if self.stop == False:
                pyautogui.click(button='left')
                pyautogui.sleep(0.11)
            else:
                pyautogui.sleep(0.1)

    # def mouse2(self):
    #     while True:
    #         if self.stop == False:
    #             pyautogui.click(button='right')
    #             pyautogui.sleep(1)
    #         else:
    #             pyautogui.sleep(0.1)

    def s1(self):
        while True:
            if self.stop == False:
                # 蓄势待发
                pyautogui.press("1")
                pyautogui.sleep(10)
            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                # 吞噬箭
                if self.firstRun:
                    self.ent()
                    self.firstRun = False
                pyautogui.keyDown("2")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("2")
                pyautogui.sleep(1.2)
            else:
                pyautogui.sleep(0.1)

    def s3(self):
        while True:
            # 烟雾弹
            if self.stop == False:
                pyautogui.press("3")
                pyautogui.sleep(1)
            else:
                pyautogui.sleep(0.1)

    def s4(self):
        while True:
            # 复仇
            if self.stop == False:
                pyautogui.press("4")
                pyautogui.sleep(19)  # 配合黄道戒指，不能浪费CDR
            else:
                pyautogui.sleep(0.1)

    def potion(self):
        while True:
            if self.stop == False:
                pyautogui.press("q")
                pyautogui.sleep(0.5)
            else:
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
