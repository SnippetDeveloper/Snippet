from sympy import *
import time
import pyperclip
x, y, z, p, q = symbols("x y z p q")
keyboard.send("ctrl+c") # type: ignore
time.sleep(0.1)
expr = pyperclip.paste()
keyboard.write(str(eval(expr))) # type: ignore