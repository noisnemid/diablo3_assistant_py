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

from ruamel.yaml import YAML
import os
from pathlib import Path
from threading import Thread,current_thread
import logging

logging.basicConfig(level=0)

import keyboard
import mouse
from time import sleep

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
    # pyautogui.click(x=coords['c1'][0], y=coords['c1'][1], button='left', _pause=False)
    # sleep(0.1)
    sleep(0.1)
    # 点击分解按钮
    mouse.move(x=coords['c2'][0], y=coords['c2'][1])
    mouse.click()

    # pyautogui.click(x=coords['c2'][0], y=coords['c2'][1], button='left', _pause=False)
    lines = (0, 2, 4, 1, 3, 5) # 跳行分解，防止重复点击到空的格子影响观感(循环的次数是一样的)
    for i in lines:
        for j in range(10):
            if not keyboard.is_pressed(args['break']):
                mouse.move(x=coords['c3'][0]+coords['c3'][2]*j, y=coords['c3'][1]+coords['c3'][2]*i)
                mouse.click()
                # pyautogui.click(x=coords['c3'][0]+coords['c3'][2]*j, y=coords['c3'][1]+coords['c3'][2]*i,
                #                 button='left', _pause=False)
                # sleep(args['interval_sec'])
                sleep(args['interval_sec'])
                keyboard.send('enter')
                # import mouse
                # mouse.mov
                # mouse.click()
                # sleep(0.04)
            else:
                break


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
                # downCode = f'pyautogui.keyDown("{key}",_pause=False)'
                # upCode = f'pyautogui.keyUp("{key}",_pause=False)'
                downCode = f'keyboard.press("{key}")'
                upCode = f'keyboard.release("{key}")'
            elif key in D3Macro.MOUSE_NAMES:
                key = key.split('_')[1]
                # downCode = f'pyautogui.mouseDown(button="{key}",_pause=False)'
                # upCode = f'pyautogui.mouseUp(button="{key}",_pause=False)'
                downCode = f'mouse.press(button="{key}")'
                upCode = f'mouse.release(button="{key}")'
            for i in range(repeat):
                eval(downCode)
                sleep(args['holds'])
                eval(upCode)

                # if args['holds'] != 0:
                #     eval(downCode)
                #     sleep(args['holds'])
                #     eval(upCode)
                # else:
                #     eval(simpCode)

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
        # pyautogui.press() supports key-lists, but it has problems for it's too fast
        for k in keys:
            keyboard.send(str(k))
            # pyautogui.press(str(k))

    def releaseAll(self):
        if not self.released:
            for k,v in self.loops.items():
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

            sleep(0.000001)
    def do1(self):
        print(f'当前宏：{self.plan_name}')

        for k, v in self.loops.items():
            Thread(target=self.loopIt, args=[k, v], name=k, daemon=True).start()

        # codes for memo
        for k in self.switches['on']:
            keyboard.add_hotkey(k, self.on)
        for k in self.switches['off']:
            keyboard.add_hotkey(k, self.off)
        for k, v in self.combos.items():
            keyboard.add_hotkey(k, self.combo, args=[v])
        for k in self.global_triggers:
            keyboard.add_hotkey(k,self.serialStrokes,args=[self.global_bullets[self.global_triggers[k]]])
        for k in self.triggers:
            keyboard.add_hotkey(k,self.serialStrokes,args=[self.loops[self.triggers[k]]])
        
        # auto decom
        keyboard.add_hotkey(self.global_plan['addons']['auto_decom']['on'],autoDecom,args=[self.global_plan['addons']['auto_decom']])

        # dual-exiting proecss: both main and sub threads are exited.
        keyboard.add_hotkey(self.switches['exit'],self.exit, suppress=True)
        print(self.switches['exit'])
        keyboard.wait(self.switches['exit'],suppress=True)

    def do2(self):
        print(f'当前宏：{self.plan_name}')

        for k, v in self.loops.items():
            Thread(target=self.loopIt, args=[k, v], name=k).start()

        while True:
            # rdk = keyboard.read_key()
            # note that 1ms is only a typical value for listening loops, you'd change it as your wish
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
                    print(type(rdk))
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

            sleep(0.05)


if __name__ == '__main__':
    plan = 'plan_法师_火鸟幻身'
    plan = 'DEVTEST'
    plan = 'plan_武僧伊娜分身速刷'
    plan = 'plan_dh_冰吞'
    D3Macro(Path(__file__).parent/'conf.yml', plan).do()
