import os,sys,time
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib2.libs.conUtils import pause
from Drawlib2.core import BufferOutput,vh,vw
from Drawlib2.pointGroupAlgorithms import *
from Drawlib2.coloring import TextObj
out = BufferOutput(vw,vh).create()

coords = beethams_line_algorithm(0,0,vw(),0)
tx = TextObj("{#ff589a}{u.2592}{r}")

out.mPut(coords,tx)
out.draw()