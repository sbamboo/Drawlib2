# python
import os,sys,subprocess
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

_loggbuff = False
_outputObj = None
_monitorProcess = None
_bufferedModes = ["Buffer","Hybrid"]
_logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground.tmp")
_monitorScript = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground_monitor.py")

_lexit = exit
def _texit():
    if os.path.exists(_logFile): os.remove(_logFile)
    _lexit()
    if _monitorProcess != None:
        _monitorProcess.terminate()
exit = _texit

def launchMonitor(out=object):
    global _loggbuff,_outputObj
    _loggbuff = True
    _outputObj = out
    try:
        out._link()
    except: pass
    _monitorProcess = subprocess.Popen([sys.executable, _monitorScript], creationflags=subprocess.CREATE_NEW_CONSOLE)

def fillMonitor(out=object,char=" "):
    out.linked.buffer.fill(char)

width = os.get_terminal_size()[0]

x,y = 0,os.get_terminal_size()[1]
prefix = "Drawlib > "

setConTitle("Drawlib Playground! (v0)")
clear()

print("Welcome to drawlib playground!")
print("Press ENTER to contine and once inside write 'exit()' to exit.")
print("\033[3m\033[90mYou can use \033[23mlaunchMonitor(<outputObj>)\033[3m to view buffered outputs memory,")
print('and \033[23mfillMonitor(<outputObj>,<char=" ">)\033[3m to fill the buffer with a char.\033[23m\033[0m')
print("-"*width)
if input("> ") == "exit()": _texit()
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
    except KeyboardInterrupt: _texit()
    try: exec(_inp)
    except Exception as e:
        if debug == True:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m\n{e}")
        else:
            print(f"\033[31mInvalid input: '{_inp}'\033[0m")
    if _loggbuff == True and _outputObj != None:
        if _outputObj.mode in _bufferedModes:
            open(_logFile,'w').write( json.dumps( _outputObj.linked.buffer.buffer ) )