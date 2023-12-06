from consoletools import sizeAssist
from core import DrawlibOut
from objects import rectangleObj
from generators import rainbowGenerator
from manip import *
from dtypes import sprite_to_cmpxPixelGroup,cmpxPixelGroup_to_splitPixelGroup,splitPixelGroup
from libs.conUtils import pause,clear

out = DrawlibOut()

rect = rectangleObj("#", 1,1, 1,10, 10,10, 10,1 ,output=out)

sprite = rect.asSprite()
sprite["tx"] = fillShape(sprite["tx"],fillChar="*")
_splitPixelGroup = cmpxPixelGroup_to_splitPixelGroup(sprite_to_cmpxPixelGroup(sprite," "))
rect.splitPixelGroup = splitPixelGroup(splitPixelGroup=_splitPixelGroup,baseColor=rect.drawData["baseColor"],palette=rect.drawData["palette"],output=rect.drawData["output"])

clear()
rect.draw()
pause()