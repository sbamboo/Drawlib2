from core import DrawlibOut,CellOpOutofBounds
from imaging import boxImage
from libs.conUtils import pause,clear
from consoletools import sizeAssist

out = DrawlibOut(mode="Buffer")

img = boxImage("C:\\Users\\simon\\Desktop\\SUNP0001_4.jpg",output=out,mode="background")

clear()
sizeAssist(*img.getSize(),out,True)

try: img.draw(0,0,drawNc=True)
except CellOpOutofBounds: pass

pause()