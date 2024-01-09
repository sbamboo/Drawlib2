import os,json

from libs.conUtils import pause
from terminal import draw

_logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"_playground.tmp")

os.system("")
while True:
    try:
        if os.path.exists(_logFile):
            data = json.loads(open(_logFile,'r').read())
            for line in data:
                yi = line
                line = data[str(line)]
                for cell in line:
                    xi = cell
                    cell = line[str(cell)]
                    draw(xi,yi,cell)
    except PermissionError: pass
    except Exception as e:
        if "Expecting value" not in str(e):
            print("Ex: "+str(e))
            pause()