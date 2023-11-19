from libs.conUtils import pause
from core import BufferOutput,vh,vw
from pointGroupAlgorithms import *
from coloring import TextObj
import time

out = BufferOutput(vw,vh).create()

coords = beethams_line_algorithm(0,0,vw(),0)
tx = TextObj("{#ff589a}{u.2592}{r}")

out.mPut(coords,"#")
out.draw()