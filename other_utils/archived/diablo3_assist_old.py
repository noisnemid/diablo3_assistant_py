"""
Diablo III Assistant Script

Version 20211104

According to good ideas of August Mao,
this script was changed to a data-driven coding pattern,
which provides a higher level of abstraction.
Ceres,Nov,2021

python libs needed:

pip install keyboard
pip install mouse
pip install ruamel.yaml

"""

from time import sleep
import pyautogui
import mouse
import keyboard
from ruamel.yaml import YAML
import os
from pathlib import Path
from threading import Thread, current_thread
import logging

logging.basicConfig(level=0)


yaml = YAML(pure=True)
yaml.sort_base_mapping_type_on_output = None
yaml.indent(mapping=2, sequence=4, offset=2)


def autoDecom(args: dict):
    # 自动分解

    scr_res = args['screen_resolution']

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

    scr_res = args['screen_resolution']

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

    coords = coords[scr_res]
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


class D3Macro():

    MOUSE_NAMES = ['mouse_left', 'mouse_right', 'mouse_middle']

    def __init__(self, config_yaml_file: os.PathLike, plan_name: str):
        # load the configuration
        self.config_yaml_file = config_yaml_file
        self.plan_name = plan_name
        with open(self.config_yaml_file, 'r', encoding='utf8') as yr:
            self.conf = yaml.load(yr)
            # print(json.dumps(self.conf, ensure_ascii=False, indent=4))
            self.global_plan = self.conf['GLOBAL']
            self.plan = self.conf[self.plan_name]

        # GLOBAL THINGS
        self.global_bullets = self.global_plan['bullets']
        self.global_triggers = self.global_plan['triggers']

        # LOCAL THINGS
        self.switches = self.plan['switches']
        self.loops = self.plan['loops']
        self.combos = self.plan['combos']
        self.triggers = self.plan['triggers']

        self.stop = True
        self.terminated = False
        self.released = False

    def on(self):
        former_state = self.stop
        self.stop = False
        if former_state == True:
            logging.info('started...')

    def off(self):
        former_state = self.stop
        self.stop = True
        if former_state == False:
            logging.info('stopped...')

    def exit(self):
        logging.info('change state to exit...')
        self.terminated = True

    def serialStrokes(self, series: list):
        for stroke in series:
            key = stroke['key']
            status = stroke['status']
            args = stroke['args']
            repeat = stroke['repeat']
            if status != 'enabled':
                sleep(0.1)  # don't forget this line!
                continue
            if 'mouse' not in key:
                downCode = f'keyboard.press("{key}")'
                upCode = f'keyboard.release("{key}")'
            elif key in D3Macro.MOUSE_NAMES:
                key = key.split('_')[1]
                downCode = f'mouse.press(button="{key}")'
                upCode = f'mouse.release(button="{key}")'
            for i in range(repeat):
                eval(downCode)
                sleep(args['holds'])
                eval(upCode)
                sleep(args['sleep_after'])

    def loopIt(self, key: str, args: dict):
        while True:
            if self.terminated:
                logging.info(f'Thread { current_thread().name } exiting...')
                break
            if self.stop == False:
                self.serialStrokes(args)
            else:
                sleep(0.1)
                self.releaseAll()

    def combo(self, keys: list):
        for k in keys:
            keyboard.send(str(k))

    def releaseAll(self):
        if not self.released:
            for k, v in self.loops.items():
                for i in v:
                    if 'mouse' not in i['key']:
                        keyboard.release(str(i['key']))
            self.released = True

    def do(self):
        print(f'当前宏：{self.plan_name}')

        for k, v in self.loops.items():
            Thread(target=self.loopIt, args=[k, v], name=k).start()

        while True:
            for rdk in self.switches['on']:
                if keyboard.is_pressed(rdk):
                    self.on()
            for rdk in self.switches['off']:
                if keyboard.is_pressed(rdk):
                    self.off()
            if keyboard.is_pressed(self.switches['exit']):
                self.exit()
                break
            for rdk in self.combos:
                if keyboard.is_pressed(rdk):
                    self.combo(self.combos[rdk])
            for rdk in self.global_triggers:
                if keyboard.is_pressed(rdk):
                    self.serialStrokes(self.global_bullets[self.global_triggers[rdk]])
            for rdk in self.triggers:
                if keyboard.is_pressed(rdk):
                    self.serialStrokes(self.loops[self.triggers[rdk]])

            # auto_decom
            if keyboard.is_pressed(self.global_plan['addons']['auto_decom']['on']):
                autoDecom(self.global_plan['addons']['auto_decom'])

            # auto_forge
            if keyboard.is_pressed(self.global_plan['addons']['auto_forge']['on']):
                autoForge(self.global_plan['addons']['auto_forge'])

            sleep(0.000001)


if __name__ == '__main__':
    plan = 'DEVTEST'
    plan = 'plan_dh_冰吞'
    plan = 'plan_法师_火鸟幻身'
    plan = 'plan_武僧伊娜分身速刷'
    D3Macro(Path(__file__).parent/'conf.yml', plan).do()
