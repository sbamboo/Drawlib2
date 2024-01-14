import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib2.core import DrawlibOut,Buffer,BufferCachedClear
from Drawlib2.terminal import reset_write_head
from Drawlib2.shapes import *
from Drawlib2.coloring import TextObj
from Drawlib2.libs.conUtils import clear,pause

from time import sleep

def bclear(output=object):
    output.clear()
    clear()

def erase(obj=object,char=" ",erraseDrawNc=True):
    oldChar = obj.char
    obj.char = char
    obj.draw(erraseDrawNc)
    obj.char = oldChar

class Clearer():
    def __init__(self,output=object,clearChar=" "):
        self.out = output
        self.clearChar = clearChar
        self.cache = self._cacheSize()
        self.clrData = None
        self.gottenBuffer = self._getBuffer()
        self._createClearData()
    def _cacheSize(self):
        width, height = self.out.getsize()
        self.cache = {"width":width,"height":height}
    def _createClearData(self):
        width, height = self.out.getsize()
        create = True
        if self.cache == None or width != self.cache["width"] or height != self.cache["height"]:
            self._cacheSize()
        elif self.clrData != None:
            create = False
        if create == True and self.gottenBuffer != None:
            # check if y-major can be assumed
                # create 
            pass
                
    def _getBuffer(self):
        buffer = None
        # check if output obj or single
        outWrapper = False
        try:
            self.out.mode
            outWrapper = True
        except: pass
        # Now check if it has a buffer
        if outWrapper == True:
            try:
                self.out.linked
            except:
                self.out._link()
            try:
                buffer = self.out.linked.buffer
            except: pass
        else:
            try:
                buffer = out.buffer
            except: pass
        return buffer
    def apply(self):
        if self.gottenBuffer != None:
            self._createClearData()
            self.gottenBuffer.buffer = self.clrData
        else:
            clear()

clear()

width, height = os.get_terminal_size()

buffer = BufferCachedClear(width,height)

out = DrawlibOut("Buffer",buffInst=buffer)
#out = DrawlibOut("Buffer")

blue  = TextObj("{f.blue}#{r}")
red   = TextObj("{f.red}@{r}")
green = TextObj("{f.green}@{r}")

ob1 = circle(blue,10,10,5,out)
ob2 = circle(red, 22,10,5,out)

delay = 0

try:
    while True:

        erase(ob2)
        reset_write_head()

        out.clear()
        ob1.draw(drawNc=True) #put
        ob2.xM = 22
        ob2.char = red
        ob2.draw(drawNc=True) #put
        out.draw(nc=True)

        sleep(delay)

        erase(ob2)
        reset_write_head()

        out.clear()
        ob1.draw(drawNc=True) #put
        ob2.xM = 24
        ob2.char = green
        ob2.draw(drawNc=True) #put
        out.draw(nc=True)

        sleep(delay)

except KeyboardInterrupt: pass