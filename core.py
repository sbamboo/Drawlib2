from types import MethodType
from libs.conUtils import clear,getConSize,setConSize
from termMethods import draw
from coloring import removeAnsiSequences

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

class Placeholders():
    def __init__(self): pass
    def vh(): pass
    def vw(): pass

placeholders = Placeholders()
vh = placeholders.vh
'''ConsoleSize.Height'''
vw = placeholders.vw
'''ConsoleSize.Width'''
del placeholders

class sp_Buffer():
    def __init__(self,width,height,iChar=" "):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        if type(width) != int:
            width = max(width)+1
        if type(height) != int:
            height = max(height)+1
        self.bufferSize = (width,height)
        self.buffer = None
        self.bufferBaseChar = iChar
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
            _buffer = []
            for y in range(self.bufferSize[-1]):
                for x in range(self.bufferSize[0]):
                    if len(_buffer)-1 < y:
                        _buffer.append(list())
                    _buffer[y].append(self.bufferBaseChar)
            self.buffer = _buffer
    def clear(self):
        if self.isCreated() == True:
            _buffer = []
            for y in range(self.bufferSize[-1]):
                for x in range(self.bufferSize[0]):
                    if len(_buffer)-1 < y:
                        _buffer.append(list())
                    _buffer[y].append(self.bufferBaseChar)
            self.buffer = _buffer
    def destroy(self):
        if self.isCreated() == True:
            self.buffer = None
    def getY(self):
        if self.isCreated() == False:
            raise UncreatedBuffer()
        return len(self.buffer)
    def getX(self):
        if self.isCreated() == False:
            raise UncreatedBuffer()
        return len(self.buffer[0])
    def getLines(self,stX=None,stY=None,enX=None,enY=None):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle st,en vals
        if type(stX) != int:
            stX = 0
        if type(stY) != int:
            stY = 0
        if type(enX) != int:
            enX = self.bufferSize[0]
        if type(enY) != int:
            enY = self.bufferSize[-1]
        # handle out-of-bounds
        self.anyOutOfBounds([stX,enX],[stY,enY])
        # fix return
        toRet = []
        for y in list(range(stY+1,enY+1)):
            y = y-1
            st = ""
            for _x in self.buffer[y][stX:enX]:
                st += str(_x)
            st = st[0:self.bufferSize[0]]
            toRet.append(st)
        return toRet
    def draw(self,stX=None,stY=None,enX=None,enY=None,nc=False):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle st,en vals
        if type(stX) != int:
            stX = 0
        if type(stY) != int:
            stY = 0
        if type(enX) != int:
            enX = self.bufferSize[0]
        if type(enY) != int:
            enY = self.bufferSize[-1]
        # handle out-of-bounds
        self.anyOutOfBounds([stX,enX],[stY,enY])
        # get lines
        lines = self.getLines(stX,stY,enX,enY)
        # print
        if nc != True: clear()
        for y in range(len(lines)+1):
            if lines[y-1].strip() != "":
                tx = lines[y-1]
                draw(0,y,tx)
    def put(self,x=int,y=int,st=str):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle out-of-bounds
        self.anyOutOfBounds([x],[y])
        # put
        ln = len(st)
        try:
            affLi = self.buffer[y]
            for i in range(ln):
                affLi[x+i] = st
            self.buffer[y] = affLi
        except:
            pass
    def getBuf(self,retEmpty=False):
        if retEmpty == True:
            return self.buffer
        cbuf = self.buffer
        for yi,y in enumerate(cbuf):
            eX = []
            for xi,x in enumerate(cbuf[yi]):
                if cbuf[yi][xi] == self.bufferBaseChar:
                    cbuf[yi][xi] = ""
                eX.append("")
            if cbuf[yi] == eX:
                cbuf[yi] = []
        return cbuf

class Buffer():
    def __init__(self,width,height):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        if type(width) != int:
            width = max(width)+1
        if type(height) != int:
            height = max(height)+1
        self.bufferSize = (width,height)
        self.buffer = None
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
     def getLines(self,stX=None,stY=None,enX=None,enY=None):
        # raise on non-created
        if self.isCreated() == False:
            raise UncreatedBuffer()
        # handle st,en vals
        if type(stX) != int:
            stX = 0
        if type(stY) != int:
            stY = 0
        if type(enX) != int:
            enX = self.bufferSize[0]
        if type(enY) != int:
            enY = self.bufferSize[-1]
        # handle out-of-bounds
        self.anyOutOfBounds([stX,enX],[stY,enY])
        # fix return
        

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
    def draw(self,x=int,y=int):
        raise UnfinishedMethod()
    def mPut(self,coords=list,st=str):
        for pair in coords:
            self.put(pair[0],pair[1],st)

class BufferOutput(Output):
    def __init__(self,width=None,height=None,name="Drawlib.Buffer.Buffer",iChar=" "):
        if height == "vh" or isinstance(height,MethodType): height = getConSize()[-1]
        if width == "vw" or isinstance(width,MethodType): width = getConSize()[0]
        super().__init__(width,height,name)
        self.buffer = Buffer(width,height,iChar)
    def create(self):
        self.buffer.create()
    def destroy(self):
        self.buffer.destroy()
    def clear(self):
        self.buffer.clear()
    def put(self,x=int,y=int,inp=str):
        self.buffer.put(x,y,st=inp)
    def draw(self,x=int,y=int,nc=False):
        self.buffer.draw(x,y,nc)
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
    def __init__(self,name="Drawlib.Buffer.Hybrid",iChar=" "):
        self.conSize = getConSize()
        super().__init__(self.conSize[0],self.conSize[-1],name)
        self.buffer = Buffer(self.conSize[0],self.conSize[-1],iChar)
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
    def draw(self,x=int,y=int,nc=False):
        self.buffer.draw(x,y,nc)
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
    def setMode(self,mode=None):
        if mode not in self.allowedMods:
            raise InvalidOutputMode()
        else:
            self.mode = mode
    def resMode(self):
        self.mode = self.defMode