from types import MethodType
from libs.conUtils import clear,getConSize,setConSize
from terminal import draw
from coloring import removeAnsiSequences,TextObj
import json,os

# region Exceptions
class InvalidOutputSize(Exception):
    def __init__(self,message="Drawlib.Output: InvalidSize!"):
        self.message = message
        super().__init__(self.message)

class UnfinishedMethod(Exception):
    def __init__(self,message="Drawlib.Output: This method has not been defined correctly!"):
        self.message = message
        super().__init__(self.message)

class UncreatedBuffer(Exception):
    def __init__(self,message="Drawlib.Buffer: Attempted call on non-created buffer!"):
        self.message = message
        super().__init__(self.message)

class CellOpOutofBounds(Exception):
    def __init__(self,message="Drawlib.Output: Attempted cell operation out of bounds!"):
        self.message = message
        super().__init__(self.message)

class InvalidOutputMode(Exception):
    def __init__(self,message="Drawlib.Output: Invalid output mode!"):
        self.message = message
        super().__init__(self.message)

class DelimToLong(Exception):
    def __init__(self,message="Drawlib.Buffer: Deliminator to long!"):
        self.message = message
        super().__init__(self.message)
# endregion

# region Placeholders
class Placeholders():
    def __init__(self): pass
    def vh(self): return os.get_terminal_size()[-1]
    def vw(self): return os.get_terminal_size()[0]

placeholders = Placeholders()
vh = placeholders.vh
'''ConsoleSize.Height'''
vw = placeholders.vw
'''ConsoleSize.Width'''
del placeholders
# endregion

# region Buffer & Output classes
class Buffer():
    def __init__(self,width,height,fallbackChar=" "):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        if type(width) != int:
            width = max(width)+1
        if type(height) != int:
            height = max(height)+1
        self.bufferSize = (width,height)
        self.buffer = None
        self.fallbackChar = fallbackChar
    def isCreated(self):
        if self.buffer == None:
            return False
        else:
            return True
    def isOutOfBoundsX(self,x):
        if x < 0 or x > self.bufferSize[0]: return True
        else: return False
    def isOutOfBoundsY(self,y):
        if y < 0 or y > self.bufferSize[1]: return True
        else: return False
    def anyOutOfBounds(self,xs=[],ys=[]):
        for x in xs:
            if self.isOutOfBoundsX(x):
                raise CellOpOutofBounds()
        for y in ys:
            if self.isOutOfBoundsY(y):
                raise CellOpOutofBounds()
    def create(self):
        if self.isCreated() == False:
            self.buffer = {}
            for y in range(self.bufferSize[1]):
                self.buffer[y] = {}
    def clear(self):
        if self.isCreated() == True:
            self.buffer = {}
            for y in range(self.bufferSize[1]):
                self.buffer[y] = {}
    def destroy(self):
        if self.isCreated() == True:
            self.buffer = None
    def put(self,x,y,st):
        self.anyOutOfBounds([x],[y])
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # put
        self.buffer[y][x] = st
    def draw(self,nc=False):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # draw
        if nc == False: clear()
        for y in self.buffer:
            for x in self.buffer[y]:
                v = self.buffer[y].get(x)
                if v == "" or v == None: v = self.fallbackChar
                draw(x,y,v)
    def putDelim(self,x,y,st,delim=";"):
        if len(delim) > 1:
            raise DelimToLong()
        st = st.replace(f"\\{delim}","§delim§")
        sst = st.split(delim)
        for i,p in enumerate(sst):
            sst[i] == p.replace("§delim§",delim)
        ln = len(st)
        for i in range(ln):
            self.put(x+i,y,sst[i])
    def putCharList(self,x,y,li=list):
        ln = len(li)
        for i in range(ln):
            self.put(x+i,y,sst[i])
    def _toStr(self) -> dict:
        data = {}
        for y in self.buffer:
            data[y] = {}
            for x in self.buffer[y]:
                v = self.buffer[y][x]
                if isinstance(v, TextObj):
                    v = v.exprt()
                    v["tag"] = 1
                else:
                    v = str(v)
                data[y][x] = v
        return data
    def exportF(self) -> str:
        return json.dumps(self._asStr())
    def importF(self,jsonStr):
        data = json.loads(jsonStr)
        for y in data:
            for x in data[y]:
                if isinstance(data[y][x], dict):
                    idata = data[y][x]
                    data[y][x] = TextObj("")
                    data[y][x].imprt(idata)
        self.buffer = data


class Output():
    def __init__(self,width=None,height=None,name="Drawlib.Buffer.Generic"):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        self.name = name
        self.width = width
        self.height = height
    def _checkSizeInit(self):
        if self.width == None or self.height == None:
            raise InvalidOutputSize(self.name+": Invalid Size!")
    def clear(self):
        raise UnfinishedMethod()
    def put(self,x=int,y=int,inp=str):
        raise UnfinishedMethod()
    def draw(self,x=int,y=int,nc=False):
        raise UnfinishedMethod()
    def mPut(self,coords=list,st=str):
        for pair in coords:
            self.put(pair[0],pair[1],st)

class BufferOutput(Output):
    def __init__(self,width=None,height=None,name="Drawlib.Buffer.Buffer", fallbackChar=" "):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        super().__init__(width,height,name)
        self.buffer = Buffer(width,height,fallbackChar=fallbackChar)
    def create(self):
        self.buffer.create()
    def destroy(self):
        self.buffer.destroy()
    def clear(self):
        self.buffer.clear()
    def put(self,x=int,y=int,inp=str):
        # put
        self.buffer.put(x,y,st=inp)
    def draw(self,nc=False):
        self.buffer.draw(nc)
        print("\033[0m")
    def getBuf(self,retEmpty=False):
        return self.buffer.getBuf(retEmpty)

class ConsoleOutput(Output):
    def __init__(self):
        self.conSize = getConSize()
        super().__init__(self.conSize[0],self.conSize[-1],None)
    def getSize(self):
        self.conSize = getConSize()
        return self.conSize
    def setSize(self,x=None,y=None):
        if x == None:
            x = self.conSize[0]
        if y == None:
            y = self.conSize[-1]
        setConSize(x,y)
    def isOutOfBoundsX(self,x):
        if x < 0 or x > self.conSize[0]: return True
        else: return False
    def isOutOfBoundsY(self,y):
        if y < 0 or y > self.conSize[1]: return True
        else: return False
    def anyOutOfBounds(self,xs=[],ys=[]):
        for x in xs:
            if self.isOutOfBoundsX(x):
                raise CellOpOutofBounds()
        for y in ys:
            if self.isOutOfBoundsY(y):
                raise CellOpOutofBounds()
    def clear(self):
        clear()
    def put(self,x=int,y=int,st=str):
        # handle out-of-bounds
        self.anyOutOfBounds([x],[y])
        # put
        draw(x,y,st)
        print("\033[0m")

class HybridOutput(Output):
    def __init__(self,name="Drawlib.Buffer.Hybrid", fallbackChar=" "):
        self.conSize = getConSize()
        super().__init__(self.conSize[0],self.conSize[-1],name)
        self.buffer = Buffer(self.conSize[0],self.conSize[-1],fallbackChar=fallbackChar)
    def getSize(self):
        self.conSize = getConSize()
        return self.conSize
    def setSize(self,x=None,y=None):
        if x == None:
            x = self.conSize[0]
        if y == None:
            y = self.conSize[-1]
        setConSize(x,y)
    def create(self):
        self.buffer.create()
    def destroy(self):
        self.buffer.destroy()
    def clear(self):
        clear()
        self.buffer.clear()
    def put(self,x=int,y=int,inp=str):
        self.buffer.put(x,y,st=inp)
        draw(x,y,inp)
    def draw(self,nc=False):
        self.buffer.draw(nc)
    def clearCon(self):
        clear()
    def clearBuf(self):
        self.buffer.clear()
    def putCon(self,x=int,y=int,inp=str):
        draw(x,y,inp)
    def putBuf(self,x=int,y=int,inp=str):
        self.buffer.put(x,y,st=inp)
    def getBuf(self,retEmpty=False):
        return self.buffer.getBuf(retEmpty)

class DrawlibOut():
    def __init__(self,mode=None,overwWidth=None,overwHeight=None,buffIChar=None):
        if overwHeight == "vh" or isinstance(overwHeight,MethodType): overwHeight = getConSize()[-1]
        if overwWidth == "vw" or isinstance(overwHeight,MethodType): overwWidth = getConSize()[0]
        self.overwWidth = overwWidth
        self.overwHeight = overwHeight
        self.buffIChar = buffIChar
        self.allowedMods = ["Buffer","Console","Hybrid"]
        self.defMode = "Console"
        if mode in self.allowedMods:
            self.mode = mode
        else:
            self.mode = self.defMode
        self.linked = None
    def setM(self,mode=None):
        if mode not in self.allowedMods:
            raise InvalidOutputMode()
        else:
            self.mode = mode
    def resM(self):
        self.mode = self.defMode
    def _link(self):
        if self.mode == "Buffer":
            width = vw
            height = vh
            if self.overwWidth != None: width = self.overwWidth
            if self.overwHeight != None: height = self.overwHeight
            self.linked = BufferOutput(width,height,fallbackChar=self.buffIChar)
        elif self.mode == "Console":
            self.linked = ConsoleOutput()
        elif self.mode == "Hybrid":
            self.linked = HybridOutput(fallbackChar=self.buffIChar)
    def put(self,x,y,st):
        if self.linked == None: self._link()
        self.linked.put(x,y,st)
    def draw(self,nc=False):
        if self.linked == None: self._link()
        self.linked.draw(nc=nc)
    def clear(self):
        if self.linked == None: self._link()
        self.linked.clear()
    def mPut(self,*args,**kwargs):
        if self.linked == None: self._link()
        self.linked.mPut(*args,**kwargs)
# endregion

# region draw functions
def base_draw(x,y,st=str,drawNc=False,overwWidth=None,overwHeight=None,mode="Console",buffIChar=" "):
    _obj = DrawlibOut(
        mode=mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar
    )
    _obj.put(x,y,st)
    if _obj.mode != "Console":
        _obj.draw(drawNc)

def base_mdraw(coords,st=str,drawNc=False,overwWidth=None,overwHeight=None,mode="Console",buffIChar=" "):
    _obj = DrawlibOut(
        mode=mode,
        overwWidth=overwWidth,
        overwHeight=overwHeight,
        buffIChar=buffIChar
    )
    _obj.mPut(coords,st)
    if _obj.mode != "Console":
        _obj.draw(drawNc)
# endregion
