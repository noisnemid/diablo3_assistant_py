import pyautogui
import keyboard
import mouse
from threading import Thread
from traceback import format_exc


'''
思路：

    游戏内 技能分配 及 循环需求 说明

        左键 百裂拳 0.1s 连点循环，触发对戒，拾取，过门
        右键 灵光悟（流沙覆） 手动，瞬移至敌怪身边
        1 飓风破 1.5s 循环 聚怪，触发对戒，可视能量回复速率调整间隔
        2 禅定 0.1s 循环，防御技
        3 疾风击 不循环，手动，游戏中和鼠标中键绑定，可单手操作
        4 幻身 0.1s 循环

脚本使用：

    F1开启，F2关闭

注意事项：

    1. 由于WIN10输入法造成脚本个别键无法循环时，重启脚本。
    2. 由于按键冲突等问题，F2停止脚本可能会不生效，多按几次F2即可。
    3. 过快点击或按键会造成一些性能或功能问题
    4. pyautogui的函数默认有0.1秒暂停间隔，可通过_pause=Fasle参数将之设置为0后使用sleep函数人工调整。
'''

# 配置部分
SCRIPT_NAME = 'diablo3-macro-武僧-伊娜水幻身速刷-S24'






class Macro(object):

    def __init__(self):
        # add the acts you wanted to do here:
        # 全局切换开关
        self.globalSwitchOn = "f1"
        self.globalSwitchOff = "f2"

        # 动作列表，不需要的注释掉
        self.acts = [
            # self.forceMove,
            self.mouse1,
            # self.mouse2,
            self.s1,
            self.s2,
            # self.s3,
            self.s4,
            self.potion
        ]

        global SCRIPT_NAME
        self.name = SCRIPT_NAME
        self.stop = True
        self.counter = 0
        self.paused = False
        self.firstRound = True

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
            pyautogui.press('space')  # 连按数次空格清除对话框
        # for i in range(6):
        #     pyautogui.keyDown("2")
        #     pyautogui.sleep(0.1)
        #     pyautogui.keyUp("2")
        print('ent ran')

    def mouse1(self):
        while True:
            if self.stop == False:
                pyautogui.click(clicks=1, button='left',
                                _pause=False)  # 频率太高会失去效果（同一坐标点击多次）
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
        # pyautogui.click(button="right")
        # pyautogui.press("`")
        print(format_exc())
