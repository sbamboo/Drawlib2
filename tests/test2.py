import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib_V2.core import DrawlibOut,CellOpOutofBounds
from Drawlib_V2.imaging import boxImage
from Drawlib_V2.libs.conUtils import pause,clear
from Drawlib_V2.consoletools import sizeAssist

out = DrawlibOut(mode="Buffer")

out._link()
width, height = out.getsize()

img = boxImage(os.path.join(parent,"test.png"),output=out,mode="foreground",width=width,height=height)

clear()
#sizeAssist(*img.getSize(),out,True)

try: img.draw(0,0,drawNc=True)
except CellOpOutofBounds: pass

out.draw()
pause()