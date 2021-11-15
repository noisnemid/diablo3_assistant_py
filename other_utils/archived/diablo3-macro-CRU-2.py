import pyautogui
import keyboard
from threading import Thread
from traceback import format_exc
'''
SCRIPTNAME=DIABLO III CRUSADER AUTO IN ONE
AUTHOR=CERES
INPIRED BY & THX TO = AUGUSTMAO
VERSION=2.0
DATE=2020-12-29

DESC：

    D3 S22 2.6.9 圣教军散件荆棘跑马炮脚本
    
    D3圣教军散件荆棘炮轰应该是最“抠脚”的BD了（当然前提是需要宏的配合）。

    使用方法：

        运行脚本后，宏处于等候状态。

        按F1开始，按F2停止。

目的：

    最大化跑马覆盖率和主动轰击。

思路：

    除左键大炮酒桶外，所有技能，持续结束立即施放，并补按跑马（因为此时跑马技能必然已被打断）。
    
    补按跑马之后，跑马技能线程重置，重新开始计时。

    左键为主动炮轰，点到敌人即为技能，点到地面即为移动，点到物品即为拾取。

详解：

    由于[梅塞施密特的劫掠者]和[寅剑]的参与，各技能CD变得波动非常大，为了梅斧的CDR效果尽量用于
    主动炮轰，其它技能在持续结束时才使用，避免无脑高频点击造成的跑速损失甚至是火力损失。

前置：

    游戏内技能设置：
    
        左键.  轰击（尖刺桶）
        右键.  挑衅（见招拆招）
        1.  钢铁之肤（反伤之肤）
        2.  希望律法（天使之翼）
        3.  战马冲锋（马不停蹄）
        4.  阿卡拉特勇士（先知化身）

其它：

    反引号键 “`”用于强制移动，在宏内为其设置为1秒持续、0.2秒暂停的节奏用于过门、拣物。
    如无法适应此节奏，将此时间比例进行微调或彻底关闭该功能。（在self.acts内注释掉self.forceMove入口即可。）
    左键中断跑马技能后暂时无法检测到，因为在不读取游戏内存数据的情况下，无法探测一个变动CDR的技能的冷却情况。

'''
pyautogui.PAUSE = 0


class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        self.stop = True
        self.skillBlk = False  # 技能阻塞，用于保护特定技能不被打断，可设置多个
        self.runReset = 0
        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"

        # 开启并行的动作进程，不需要的进程注释掉即可
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
                pyautogui.sleep(1)
            else:
                pyautogui.sleep(0.1)

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
                self.runReset = -1  # 补充跑马
                pyautogui.sleep(2.9)
            else:
                pyautogui.sleep(0.1)

    def s1(self):
        # 可以打断S2，帮不需要检测skillBlk值但是需要等待持续结束
        while True:
            if self.stop == False:
                pyautogui.press("1")
                self.runReset = -1  # 补充被打断的跑马技能
                pyautogui.sleep(2.9)
            else:
                pyautogui.sleep(0.1)

    def s2(self):
        while True:
            if self.stop == False:
                pyautogui.press("2")
                self.runReset = -1  # 补充跑马
                pyautogui.sleep(2.9)
            else:
                pyautogui.sleep(0.1)

    def s3(self):
        # 速移技能，此技能不能被特定技能打断
        while True:
            if self.stop == False:
                if self.runReset % 29 == 0:
                    pyautogui.press("3")
                    pyautogui.click(button='left')
                self.runReset = self.runReset + 1
                pyautogui.sleep(0.1)
            else:
                pyautogui.sleep(0.1)

    def s4(self):
        # 因不能浪费CDR，故要严格按照持续时间来，从而可以在持续结束的时候打断S3并使用。
        while True:
            if self.stop == False:
                pyautogui.press("4")
                self.runReset = -1  # 补充跑马技能
                pyautogui.sleep(5)
            else:
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
        m.start() # 开启进程

        print('watching...')
        m.watcher() # 宏全局切换开关快捷键监听

    except Exception as e:
        pyautogui.click(button="right")
        pyautogui.press("`")
        print(format_exc())
