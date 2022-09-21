import pyautogui
import keyboard
import mouse
from threading import Thread
from traceback import format_exc
'''
D3 DH 冰吞 大/小密境 全自动 通用脚本

思路：

    游戏内技能分配

        左键 宠物
        右键 回能
        1 扫射
        2 吞噬
        3 烟雾
        4 复仇

        1、2技能 吞噬箭、扫射组合序列，因为吞噬箭会打断扫射，而长时间扫射会有几率导致吞噬箭无法触发。
        3  扫射， 以长时间按压、短时间停
        3，4，辅助技能
        左键为宠物召唤技能，点到敌人即为技能，点到地面即为移动，点到物品即为拾取。
        2. 
    
        其它技能，CD完毕立即使用即可。

            特别注意右键可以严格按照CD时间来使用或适当加大间隔，因为如果在调用地图期间仍然高频率按动右键会将地图界面关闭

'''

pyautogui.FAILSAFE = False

class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.name = "D3 DH 冰吞 大/小密境 全自动 通用脚本"
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
        # 进场动作，叠层7次
        # pyautogui.sleep(0.2)
        for i in range(3):
            pyautogui.press('space')
        for i in range(6):
            pyautogui.keyDown("2")
            pyautogui.sleep(0.1)
            pyautogui.keyUp("2")
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
                    pyautogui.sleep(1.1)
                    pyautogui.keyUp("1")
                else:
                    self.pause(1.33, 's1')

                pyautogui.keyDown("2")
                pyautogui.sleep(0.133)
                pyautogui.keyUp("2")
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
