import pyautogui
from threading import Thread
from traceback import format_exc
import keyboard
'''
DESC

NAME = D3 NEC S22速刷辅助按键脚本
AUTHOR = CERES
DATE = 2020-12-26
VER = 2.0

游戏内技能设置：

    依次为1，2，3，4，鼠左，鼠右

    衰老，骨刺，血步，分身；骨矛，骨甲

思路：

    1.5秒间隔释放1技能，1秒间隔2技能

    点指敌人释放左键技能，点指地面移动

    点指物品拾取。其它技能手动。


'''

class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.stop = True

        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"
        self.globalSwitchPause = "f3"
        self.firstRun = True

        self.acts = [
            # self.forceMove,
            self.ent,
            self.mouse1,
            self.mouse2,
            # self.s1,
            # self.s2,
            # self.s3,
            # self.s4,
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
                pyautogui.sleep(0.5)
            else:
                pyautogui.sleep(0.2)

    def ent(self):
        # 进场动作
        while True:
            if self.stop == False:
                if self.firstRun:
                    pyautogui.press("4")
                    self.firstRun = False
            pyautogui.sleep(0.4)

    def mouse1(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='left')
                # pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def mouse2(self):
        while True:
            if self.stop == False:
                pyautogui.click(button='right')
                pyautogui.sleep(4)
            else:
                pyautogui.sleep(0.1)

    def s1(self):
        # 覆盖S2，S2不再添加到序列中
        while True:
            if self.stop == False:
                if self.firstRun:
                    self.ent()
                    self.firstRun = False
                pyautogui.keyDown("1")
                pyautogui.sleep(1.2)
                pyautogui.keyUp("1")
                pyautogui.keyDown("2")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("2")
            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("2")
                pyautogui.sleep(0.1)
                pyautogui.keyUp("2")
                pyautogui.sleep(2)
            else:
                pyautogui.sleep(0.1)

    def s3(self):
        while True:
            if self.stop == False:
                pyautogui.press("3")
                pyautogui.sleep(1)
            else:
                pyautogui.sleep(0.1)

    def s4(self):
        while True:
            if self.stop == False:
                pyautogui.press("4")
                pyautogui.sleep(0.5)
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
