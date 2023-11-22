from core import DrawlibOut
from libs.conUtils import pause,clear
from coloring import TextObj
from shapes import triangle

clear()

out = DrawlibOut(mode="Console")

tx = TextObj("{b.blue} {r}")

tri = triangle(tx, 10,6, 20,6, 15,1, out)

tri.draw()

pause()