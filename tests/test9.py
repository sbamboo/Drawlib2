import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib2.graphing import graphPlotter
from Drawlib2.core import DrawlibOut
from Drawlib2.libs.conUtils import clear,pause

out = DrawlibOut(mode="Buffer")

clear()

graph = graphPlotter("f(x)=x^2",out)

graph.plot(
    pos = (0,0),
    xRange = (-10,10),
    yRange = (-10,10),
    step = 1,
    xFactor = 1.0,
    yFactor = 1.0,
    floatRndDecis = 2,
    intRound = True,
    assumptionFill = True,
    debug = False,
    debug_x_scale = 1.0,
    debug_y_scale = 1.0,
    debugGrid = True
)

#graph.put()

print(graph.getAsTx())

#out.draw()

pause()