import pyautogui
import keyboard
import mouse
from threading import Thread
from traceback import format_exc
'''
D3 法师火鸟聚能球 S24 通用脚本

思路：

    游戏内技能分配

        3/中键 传送
        右键 引导
        1 聚能
        2，4 ，左键状态

'''


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.name = "D3 法师火鸟聚能球 S24 通用脚本"
        self.stop = True
        self.counter = 0
        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"

        self.globalSwitchPause = "ctrl"  # 该功能用于暂停1.1秒拣物/过门
        self.paused = False

        self.firstRound = True

        self.acts = [
            # self.forceMove,
            # self.mouse1,
            # self.mouse2,
            self.s1,
            self.s2,
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
                self.firstRound = True
                self.stop = False
                self.paused = False
                self.counter = self.counter + 1
            if keyboard.is_pressed(self.globalSwitchOff):
                self.stop = True
            if keyboard.is_pressed(self.globalSwitchPause):
                self.paused = True

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
        # pyautogui.sleep(0.2)
        for i in range(3):
            pyautogui.press('space')
        pyautogui.keyDown("2")
        pyautogui.sleep(0.1)
        pyautogui.keyUp("2")
        pyautogui.sleep(0.1)
        pyautogui.keyDown("4")
        pyautogui.sleep(0.1)
        pyautogui.keyUp("4")
        
        print('ent ran')

    def mouse1(self):
        while True:
            if self.stop == False:
                pyautogui.click(clicks=1, button='left', _pause=False)  # 频率太高会失去效果（同一坐标点击多次）
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
                if self.firstRound == True:
                    self.ent()
                    self.firstRound = False

                if self.paused == False:
                    pyautogui.keyDown("1")
                    pyautogui.sleep(0.1)
                    pyautogui.keyUp("1")
                else:
                    self.pause(1.33, 's1')

                pyautogui.keyDown("1")
                pyautogui.sleep(0.133)
                pyautogui.keyUp("1")
            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.keyDown("3") # 保持
                pyautogui.sleep(0.1)
            else:
                pyautogui.keyUp("3")
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

    def pause(self, pause_sec, trigger='default'):
        print(f'pausing...{pause_sec} secs, triggered by {trigger}')
        pyautogui.sleep(pause_sec)
        self.paused = False

    def start(self):
        print(self.name)
        for a in self.acts:
            x = Thread(target=a)
            x.start()
        self.watcher()


if __name__ == "__main__":
    try:
        m = Macro()
        m.start()

    except Exception as e:
        pyautogui.click(button="right")
        pyautogui.press("`")
        print(format_exc())
