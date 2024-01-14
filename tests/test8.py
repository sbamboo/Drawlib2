import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib_V2.core import DrawlibOut
from Drawlib_V2.assets import asset
from Drawlib_V2.libs.conUtils import clear,pause

out = DrawlibOut(mode="Buffer")

clear()

_asset = asset(os.path.join(parent,"test.asset"),output=out)
_asset.render_put()

out.draw()