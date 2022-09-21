import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
'''
D3 DH 火多重小密境专用

SCRIPTNAME=DIABLO III DEMON HUNTER FIRE
AUTHOR=CERES
VERSION=1.0
DATE=2020-12-30

DESC：

    使用方法：

        运行脚本后，宏处于等候状态。

        按F1开始，按F2停止。ctrl暂停

目的：

    鉴于冰吞快速移动期间拣东西非常麻烦，改用火多重刷小密境

前置：

    游戏内技能设置：
    
        左键.  多重
        右键.  翻滚
        1.  宠物
        2.  闪避射击
        3.  暗影之力
        4.  复仇

其它：

    反引号键 “`”用于强制移动，在宏内为其设置为1秒持续、0.2秒暂停的节奏用于过门、拣物。
    如无法适应此节奏，将此时间比例进行微调或彻底关闭该功能。（在self.acts内注释掉self.forceMove入口即可。）

'''


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.stop = True

        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"
        self.globalSwitchPause = "ctrl"
        self.firstRun = True

        self.acts = [
            # self.forceMove,
            self.mouse1,
            self.mouse2,
            self.s1,
            self.s2,
            # self.s3,
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
                self.firstRun = True
            if keyboard.is_pressed(self.globalSwitchPause):
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
            else:
                pyautogui.sleep(0.2)

    def ent(self):
        # 进场动作
        for i in range(10):
            pyautogui.keyDown("2")
            pyautogui.sleep(0.1)
            pyautogui.keyUp("2")

    def mouse1(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='left')
                pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def mouse2(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='right')
                pyautogui.sleep(5)
            else:
                pyautogui.sleep(0.1)

    def s1(self):
        # 覆盖S2，S2不再添加到序列中
        while True:
            if self.stop == False:
                pyautogui.keyDown("1")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("1")
                pyautogui.sleep(0.9)
            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("2")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("2")
            else:
                pyautogui.sleep(0.1)

    def s3(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("3")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("3")
                pyautogui.sleep(0.9)
            else:
                pyautogui.sleep(0.1)

    def s4(self):
        while True:
            if self.stop == False:
                pyautogui.press("4")
                pyautogui.sleep(0.2)
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
