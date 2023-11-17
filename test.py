from libs.conUtils import pause
from core import BufferOutput,vh,vw
from pointGroupAlgorithms import *
from coloring import TextObj
import time

out = BufferOutput(vh,vw)
out.create()

coords = simple_triangle(10,10, 20,0, 30,10)
tx = TextObj("{b.red} {r}")
tx2 = TextObj("{b.blue} {r}")

out.clear()
out.mPut(coords,tx)
out.draw()
pause()