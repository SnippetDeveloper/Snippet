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