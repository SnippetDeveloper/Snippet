import pyautogui
import keyboard
hotkeyId = -1
pyautogui.PAUSE = 0

stopKey = ""

def matching(hotkey, target = None):
    if target != None: keyboard.add_hotkey(hotkey=hotkey, callback=target)
    else: 
        global stopKey
        stopKey = hotkey
hotkeyId = 0
from sympy import *
import time
import pyperclip
x, y, z, p, q = symbols("x y z p q")
keyboard.send("ctrl+c") # type: ignore
time.sleep(0.1)
expr = pyperclip.paste()
keyboard.write(str(eval(expr))) # type: ignore
if stopKey != "": keyboard.wait(stopKey)