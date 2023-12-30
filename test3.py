from core import DrawlibOut
from terminal import reset_write_head
from shapes import *
from coloring import TextObj
from libs.conUtils import clear

clear()

out = DrawlibOut("Buffer")

blue = TextObj("{f.blue}#{r}")
red  = TextObj("{f.red}@{r}")

ob1 = circle(blue,10,10,5,out).draw(drawNc=True,supressDraw=True)
ob1

try:
    while True:
        reset_write_head()
        out.draw(nc=True)
except KeyboardInterrupt:
    pass