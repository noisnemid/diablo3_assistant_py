import pyautogui
import keyboard
import mouse
from threading import Thread
from traceback import format_exc
'''
diablo3-macro-武僧-伊娜火幻身-S24 辅助脚本

思路：

    游戏内 技能分配 及 脚本功能说明

        3 4和鼠标右键不停按
        1 每隔1s一次
        2 每隔0.5s一次
        左键连点

        左键 循环
        右键 循环
        1 每1秒循环
        2 每0.5秒循环
        3 循环
        4 循环

脚本使用：

    F1开启，F2关闭。CTRL 暂停 1 技能 1.33秒。

注意事项：

    1. 由于WIN10输入法造成脚本个别键无法循环时，重启脚本。
    2. 由于按键冲突等问题，F2停止脚本可能会不生效，多按几次F2即可。




'''

pyautogui.FAILSAFE = False

class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.name = "diablo3-macro-武僧-伊娜火幻身-S24 辅助脚本"
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
            self.mouse1,
            self.mouse2,
            self.s1,
            # self.s2,
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
            pyautogui.press('space') # 连按数次空格清除对话框
        # for i in range(6):
        #     pyautogui.keyDown("2")
        #     pyautogui.sleep(0.1)
        #     pyautogui.keyUp("2")
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
                pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def s1(self):
        # 1号技能

        while True:
            if self.stop == False:
                if self.firstRound == True:
                    self.ent()
                    self.firstRound = False

                if self.paused == False:
                    pyautogui.press("1")
                    pyautogui.sleep(1.0)
                else:
                    self.pause(1.33, 's1')

            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.press("2")
                pyautogui.sleep(0.5)
            else:
                pyautogui.sleep(0.1)

    def s3(self):
        while True:
            if self.stop == False:
                pyautogui.press("3")
                pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def s4(self):
        while True:
            if self.stop == False:
                pyautogui.press("4")
                pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def potion(self):
        # 药水
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
