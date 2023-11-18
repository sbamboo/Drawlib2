class CoreSPBuffer():
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