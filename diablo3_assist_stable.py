"""
DIABLO III ASSISTANT SCRIPT

VERSION 20211108-Stable

"""

from time import sleep
import json
import mouse
import keyboard
from ruamel.yaml import YAML
import os
from pathlib import Path
from threading import Condition, Lock, Thread, current_thread, Event
import logging

'''
SOME CONSTANTS

logging levels

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

MOUSE_NAMES = ['mouse_left', 'mouse_right', 'mouse_middle']

'''


def logId():
    n = 0
    while True:
        n += 1
        yield hex(n)


LOG_ID = logId()

logging.basicConfig(
    level='DEBUG',  # 日志级别  INFO/DEBUG 等。
    format='%(id)s > %(asctime)s - %(filename)s, line:%(lineno)d > %(levelname)s: %(message)s',
    # filename=lambda x: os.path.abspath(x)
)

yaml = YAML(pure=True)
yaml.sort_base_mapping_type_on_output = None
yaml.indent(mapping=2, sequence=4, offset=2)

# addons, standalone functions


def autoDecom(args: dict):
    # 自动分解
    coords = {
        '1920x1080': {
            'c1': [520, 480],
            'c2': [160, 300],
            'c3': [1427, 584, 50]  # top-left item cell x,y,width(height) （it's a square）
        },
        '2240x1400': {
            'c1': [667, 627],
            'c2': [215, 376],
            'c3': [1600, 760, 66]
        }
    }

    scr_res = args['screen_resolution']
    coords = coords[scr_res]

    # 调出分解界面
    mouse.move(x=coords['c1'][0], y=coords['c1'][1])
    mouse.click()
    sleep(0.1)
    # 点击分解按钮
    mouse.move(x=coords['c2'][0], y=coords['c2'][1])
    mouse.click()
    sleep(0.1)
    lines = (0, 2, 4, 1, 3, 5)  # 跳行分解，防止重复点击到空的格子影响观感(循环的次数是一样的)
    for i in lines:
        for j in range(10):
            if not keyboard.is_pressed(args['break']):
                mouse.move(x=coords['c3'][0]+coords['c3'][2]*j, y=coords['c3'][1]+coords['c3'][2]*i)
                mouse.click()
                sleep(args['interval_sec'])
                keyboard.send('enter')
            else:
                break


def autoForge(args: dict):
    # 魔盒自动打造
    coords = {
        '1920x1080': {
            'c1': [722, 839],  # “放入材料”按钮
            'c2': [236, 828],  # “接受”按钮
            'c3': [1427, 584, 50],  # top-left item cell x,y,width(height) （it's a square）
            'c4': [582, 839],  # 配方向左 按钮
            'c5': [852, 839]  # 配方向右 按钮
        },
        '2240x1400': {
            'c1': [923, 1088],  # “放入材料”按钮
            'c2': [307, 1073],  # “接受”按钮
            'c3': [1600, 760, 66],  # 装备栏
            'c4': [757, 1088],  # 配方向左 按钮
            'c5': [1103, 1088]  # 配方向右 按钮
        }
    }

    scr_res = args['screen_resolution']
    coords = coords[scr_res]

    logging.debug(f'autoForge:{coords}', extra={'id': next(LOG_ID)})

    lines = (0, 2, 4, 1, 3, 5)  # 跳行，防止重复点击到空的格子影响观感(循环的次数是一样的)
    for i in lines:
        for j in range(10):
            if not keyboard.is_pressed(args['break']):

                # 放入材料
                mouse.move(*coords['c1'])
                mouse.click()
                sleep(0.05)

                # 放入目标装备
                mouse.move(x=coords['c3'][0]+coords['c3'][2]*j, y=coords['c3'][1]+coords['c3'][2]*i)
                mouse.click(button='right')
                sleep(0.05)

                # 点击确定/接受按钮
                mouse.move(*coords['c2'])
                mouse.click()
                sleep(0.2)

                # 快速切换配方以接收装备
                mouse.move(*coords['c4'])
                mouse.click()
                sleep(0.05)
                mouse.move(*coords['c5'])
                mouse.click()
                sleep(0.05)
            else:
                break
            sleep(args['interval_sec'])

class Stroke:
    def __init__(self, stroke: dict):
        # about the stroke data scheme, see the conf.yml
        # super().__init__()
        self.__dict__.update(stroke)
        if 'mouse' in self.key:
            self.mouse_key = self.key.split('_')[1]
            self.dev_type = 'mouse'
            self.force_holding = False
        else:
            self.dev_type = 'keyboard'
        logging.debug(f'Stroke: {self.__dict__}', extra={'id': next(LOG_ID)})

    def stroke(self):
        if self.status == 'enabled':
            self.keyDown()
            self.sleep(self.hold_sec)
            self.keyUp()
            self.sleep(self.wait_after_sec)
        else:
            self.sleep(0.1)

    def keyDown(self):
        if self.status == 'enabled':
            if 'mouse' not in self.key:
                keyboard.press(self.key)
            else:
                mouse.press(button=self.mouse_key)

    def keyUp(self):
        if self.status == 'enabled':
            if 'mouse' not in self.key:
                keyboard.release(self.key)
            else:
                mouse.release(button=self.mouse_key)

    def release(self):
        if self.status == 'enabled':
            logging.debug(f'STROKE {self.key} releasing...', extra={'id': next(LOG_ID)})
            self.keyUp()
            # self.set()


class D3Macro():
    def __init__(self, config_yaml_file: os.PathLike, plan_name: str):
        # load the configuration
        self.config_yaml_file = config_yaml_file
        self.plan_name = plan_name
        with open(self.config_yaml_file, 'r', encoding='utf8') as yr:
            self.conf = yaml.load(yr)
            logging.debug(json.dumps(self.conf, ensure_ascii=False, indent=4), extra={'id': next(LOG_ID)})
            self.global_plan = self.conf['GLOBAL']
            self.plan = self.conf[self.plan_name]

        # THREADING THINGS
        self.events = {
            'exit': Event()
        }
        self.stopped = True  # 初始状态为停止状态

        self.condition = Condition(Lock())

        # GLOBAL THINGS
        # self.global_bullets = self.global_plan['bullets']
        self.global_triggers = self.global_plan['triggers']

        # LOCAL THINGS
        self.switches = self.plan['switches']

        self.loops = self.plan['loops']
        self.loop_strokes = {}

        self.combos = self.plan['combos']
        # self.triggers = self.plan['triggers']

        # REGISTER STROKE OBJECTS
        self.regLoopStrokes()

    def regLoopStrokes(self):
        for name, loop in self.loops.items():
            for stroke in loop:
                name = stroke['key']
                stk = Stroke(stroke)
                self.loop_strokes[name] = stk

    def on(self, event: keyboard.KeyboardEvent = None):
        while True:
            if self.condition.acquire():
                if self.stopped:
                    self.stopped = False
                    self.condition.notify_all()
                    logging.info('Turn ON!', extra={'id': next(LOG_ID)})
                self.condition.release()
                break

    def off(self, event: keyboard.KeyboardEvent = None):
        for name in self.loop_strokes:
            self.loop_strokes[name].release()
        while True:
            if self.condition.acquire():
                if not self.stopped:
                    self.stopped = True
                    self.condition.notify_all()
                    logging.info('Turned OFF.', extra={'id': next(LOG_ID)})
                self.condition.release()
                break

    def exit(self, event: keyboard.KeyboardEvent = None):
        self.off()
        self.events['exit'].set()
        logging.info('Exited.', extra={'id': next(LOG_ID)})

    def combo(self, event: keyboard.KeyboardEvent = None):
        key = event.name
        if key in self.combos.keys():
            for k in self.combos[key]:
                keyboard.send(str(k))
                # sleep(0.1)

    def pullOneBulletLoop(self, event: keyboard.KeyboardEvent = None):
        # mind that this only runs one of the loops of the bullet, no parallels!
        loopOnce = self.global_triggers[event.name]
        _ev = Event()
        for stroke in loopOnce:
            stk = Stroke(stroke)
            _ev.clear()
            logging.debug(stk.__dict__, extra={'id': next(LOG_ID)})
            while not _ev.is_set():
                for i in range(stk.repeat):
                    stk.keyDown()
                    _ev.wait(stk.hold_sec)
                    stk.keyUp()
                    _ev.wait(stk.wait_after_each_release_sec)
                _ev.wait(stk.wait_after_repeat_sec)
                _ev.set()
                break

    def loopIt(self, key: str, loop: dict):
        # mind that the wait() must be in the 'current' thread,
        # or it will be in a sub-thread and 'sleeping' will fail
        while True:
            if self.condition.acquire():
                if self.stopped == True:
                    self.condition.wait()
                else:
                    logging.debug(f'Thread { current_thread().name} starts-->', extra={'id': next(LOG_ID)})
                    for stroke in loop:
                        stk = self.loop_strokes[stroke['key']]
                        for i in range(stk.repeat):
                            stk.keyDown()
                            self.condition.wait(stk.hold_sec)
                            stk.keyUp()
                            self.condition.wait(stk.wait_after_each_release_sec)
                        self.condition.wait(stk.wait_after_repeat_sec)
                self.condition.release()

    def registerHotKeys(self):
        # switches
        for rdk in self.switches['on']:
            keyboard.on_release_key(rdk, self.on)
        for rdk in self.switches['off']:
            keyboard.on_release_key(rdk, self.off)
        # note that exit is a special thing
        keyboard.on_release_key(self.switches['exit'], self.exit)
        keyboard.add_hotkey('ctrl+q', self.exit, args=())

        logging.debug(self.combos, extra={'id': next(LOG_ID)})
        for k, v in self.combos.items():
            keyboard.on_release_key(k, self.combo)

        for rdk in self.global_triggers:
            keyboard.on_release_key(rdk, self.pullOneBulletLoop)

        # addons
        for addon_name, setup in self.global_plan['addons'].items():
            addon_func = globals()[addon_name] # 同名函数，这就是为什么conf.py中的GLOBAL中的键值不能随便改：因为这里会被作为函数名称使用。
            keyboard.add_hotkey(
                setup['on'],
                addon_func,
                args=(setup,),
            )
        keyboard.wait(self.switches['exit'])

    def do(self):
        logging.info(f'CURRENT RUNNING MACRO：{self.plan_name}', extra={'id': next(LOG_ID)})
        for k, v in self.loops.items():
            Thread(target=self.loopIt, args=[k, v], name=k, daemon=True).start()
        Thread(target=self.registerHotKeys, daemon=True).start()

        while not self.events['exit'].is_set():
            self.events['exit'].wait()
        else:
            logging.info('Program Terminated.', extra={'id': next(LOG_ID)})


if __name__ == '__main__':
    plan = 'DEVTEST'
    plan = 'plan_dh_冰吞'
    plan = 'plan_法师_火鸟幻身'
    plan = 'plan_武僧伊娜分身速刷(火)'
    plan = 'plan_武僧伊娜分身速刷(水)'
    plan = 'plan_武僧伊娜分身速刷(速)'
    D3Macro(Path(__file__).parent/'conf.yml', plan).do()
