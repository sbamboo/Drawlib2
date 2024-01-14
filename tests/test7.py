import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib_V2.objects import rectangleObj2
from Drawlib_V2.core import DrawlibOut
from Drawlib_V2.generators import rainbowGenerator

out = DrawlibOut(mode="Buffer")

rect = rectangleObj2("#",(0,0),(10,10),output=out,charFunc=rainbowGenerator)

rect.put()

out.draw()