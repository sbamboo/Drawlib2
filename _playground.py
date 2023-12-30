# python
import os
# libs
from libs.conUtils import *
from libs.crshpiptools import *
from libs.stringTags import *
# drawlib
from assets import *
from coloring import *
from consoletools import *
from core import *
from dtypes import *
from fonts import *
from generators import *
from imaging import *
from linedraw import *
from manip import *
from objects import *
from pointGroupAlgorithms import *
from shapes import *
from terminal import *

class RaisingDummyObject:
    '''LimitExec: Dummy object, raises.'''
    # Subscribable
    def __getitem__(self, key):
        raise NameError("Callable '"+key+"' Not found in restricted session.")
    # Callable
    def __call__(self, *args, **kwargs):
        raise NameError()
_print = print
_exit = exit
globals()['__builtins__'] = RaisingDummyObject()
globals()['__import__'] = RaisingDummyObject()
print = _print
exit = _exit

width = os.get_terminal_size()[0]

x,y = 0,os.get_terminal_size()[1]
prefix = "Drawlib > "

setConTitle("Drawlib Playground! (v0)")
clear()

print("Welcome to drawlib playground!")
print("Press ENTER to contine and once inside write 'exit()' to exit.")
print("-"*width)
if input("> ") == "exit()": exit()
clear()

while True:
    reset_write_head()
    debug = False
    try:
        draw(x,y," "*width)
        _inp = inputAtPos(x,y,prefix)
        if "deb:" in _inp:
            debug = True
            _inp = _inp.replace("deb:","").strip()
        if "clr:" in _inp:
            clear()
            _inp = _inp.replace("clr:","").strip()
    except KeyboardInterrupt: exit()
    try: exec(_inp)
    except Exception as e:
        if debug == True:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m\n{e}")
        else:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m")