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
_str = str
_int = int
_list = list
_dict = dict
_set = set
_float = float
_tuple = tuple
_bool = bool
_range = range
_len = len
_max = max
_min = min
_round = round
_abs = abs
_ord = ord
_chr = chr
globals()['__builtins__'] = RaisingDummyObject()
globals()['__import__'] = RaisingDummyObject()
print = _print
exit = _exit
str = _str
int = _int
list = _list
dict = _dict
set = _set
float = _float
tuple = _tuple
bool = _bool
range = _range
len = _len
max = _max
min = _min
round = _round
abs = _abs
ord = _ord
chr = _chr

_loggbuff = False
_outputObj = None
_monitorProcess = None
_bufferedModes = ["Buffer","Hybrid"]
_logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground.tmp")
_monitorScript = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground_monitor.py")

_waitingMonitor = True
if "--autoMon" in sys.argv:
    _waitingMonitor = False
_sizeMonitor = False
if "--sizeMon" in sys.argv:
    _sizeMonitor = True
if "--help" in sys.argv or "-h" in sys.argv or "--h" in sys.argv or "-help" in sys.argv:
    print(f"\nUsage: {os.path.basename(sys.executable)} {os.path.basename(__file__)} [--autoMon] [--sizeMon]")
    print("\nAutoMon:\n    Starts any monitor instance in auto mode, meaning it will not wait for input before drawing the buffer. (<outputObj>.clear() won't affect monitor)")
    print("SizeMon:\n    Starts any monitor instance with the size of the buffer.\n")
    exit()

_playground_internal_python_org_exit = exit
def _texit():
    global _monitorProcess
    if _monitorProcess != None:
        _monitorProcess.terminate()
        _monitorProcess = None
    if os.path.exists(_logFile): os.remove(_logFile)
    clear()
    _playground_internal_python_org_exit()
exit = _texit

def launchMonitor(out=object):
    global _loggbuff,_outputObj,_monitorProcess
    _loggbuff = True
    _outputObj = out
    try:
        out._link()
    except: pass
    _sname = str(_outputObj).replace("<","@a").replace(">","@b").replace(" ","@s").replace("'","@q").replace('"','@d')
    _pargs = [sys.executable, _monitorScript, "-oname",_sname, "-wmon",str(_waitingMonitor), "-omode",str(_outputObj.mode)]
    if _sizeMonitor == True:
        _width, _height = out.getsize()
        _pargs.extend(["-xdim",str(_width), "-ydim",str(_height)])
    _monitorProcess = subprocess.Popen(_pargs, creationflags=subprocess.CREATE_NEW_CONSOLE)

def fillMonitor(out=object,char=" "):
    global _outputObj
    if out == None:
        _outputObj.linked.buffer.fill(char)
    else:
        out.linked.buffer.fill(char)

def killMonitor(*args,**kwargs):
    global _monitorProcess
    if _monitorProcess != None:
        _monitorProcess.terminate()
        _monitorProcess = None

width = os.get_terminal_size()[0]

x,y = 0,os.get_terminal_size()[1]
prefix = "Drawlib > "

setConTitle("Drawlib Playground! (v0)")
clear()

print("Welcome to drawlib playground!")
print("Press ENTER to contine and once inside write 'exit()' to exit.")
print("\033[3m\033[90mYou can use \033[23mlaunchMonitor(<outputObj>)\033[3m to view buffered outputs memory,")
print('and \033[23mfillMonitor(<outputObj>,<char=" ">)\033[3m to fill the buffer with a char,')
print('aswell as \033[23mkillMonitor(<optional:outputObj>)\033[3m to kill the monitor.\033[23m\033[0m')
print("-"*width)
try:
    if input("ENTER/stCmd > ") == "exit()": _texit()
except KeyboardInterrupt: _texit()
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
            if "launchMonitor(" in _inp and ";" not in _inp: pass
            else:
                open(_logFile,'w').write( json.dumps( _outputObj.linked.buffer.buffer ) )