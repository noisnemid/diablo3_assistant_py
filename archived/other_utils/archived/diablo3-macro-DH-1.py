import pyautogui
from subprocess import threading,call
from threading import Thread
from time import sleep
from os import system
from traceback import format_exc

def m1():
    pyautogui.click(x=None, y=None, clicks=100000, interval=0.1, button='left', duration=0.0, tween=pyautogui.linear)

def m2():
    while True:
        pyautogui.press("2",interval=0.1)
        pyautogui.press("3",interval=0.1)
        pyautogui.press("4",interval=0.1)
        pyautogui.press("q",interval=0.1)

def m3():
    while True:
        # pyautogui.mouseDown(button="right")
        # sleep(1.2)
        # pyautogui.mouseUp(button="right")
        pyautogui.keyDown("1")
        sleep(0.2)
        pyautogui.keyUp("1")
        sleep(0.8)

def main():
    sleep(1)

    a = Thread(target=m1)
    b = Thread(target=m2)
    c = Thread(target=m3)
    a.start()
    b.start()
    c.start()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pyautogui.click(button="right")
        print(format_exc())
        system("pause")
