from core import DrawlibOut,CellOpOutofBounds
from imaging import boxImage
from libs.conUtils import pause,clear
from consoletools import sizeAssist

out = DrawlibOut(mode="Buffer")

out._link()
width, height = out.linked.buffer.bufferSize

img = boxImage("C:\\Users\\simon\\Desktop\\SUNP0001_4.jpg",output=out,mode="foreground",width=width,height=height)

clear()
#sizeAssist(*img.getSize(),out,True)

try: img.draw(0,0,drawNc=True)
except CellOpOutofBounds: pass

out.draw()
pause()