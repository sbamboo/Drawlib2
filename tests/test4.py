# Import PREP
import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

# Import
from Drawlib2.core import DrawlibOut
from Drawlib2.imaging import boxImage
from Drawlib2.libs.conUtils import clear,pause
from Drawlib2.manip import stretchShapeXlp,fixPostStretchLPcorner

# Create a output object and use "_link()" to ensure its initialized.
out = DrawlibOut(mode="Buffer")
out._link()

# Load an image 
img = boxImage(os.path.join(parent,"test2.png"),output=out,mode="foreground")

# Clear the console
clear()

# Draw the texture and wait
img.draw(0,0)
pause()

# clear
clear()

# Now use manip to stretch it
sprite = img.asSprite() # Get data as sprite
texture = stretchShapeXlp(sprite["tx"]) # Stretch it using manip.stretchShapeXlp()
img.texture = texture

# Draw
img.draw(0,0)