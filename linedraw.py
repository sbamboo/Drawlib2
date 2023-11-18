from core import base_draw,base_fill,vw,vh

def move_write_head(x=int,y=int):
    line = "\033[{};{}H".format(x,y)
    print(line)

def fill_terminal(st=str,overwWidth=None,overwHeight=None,mode=None,drawNc=False,buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    base_fill(st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)

def draw_point(x,y,st=str,overwWidth=None,overwHeight=None,drawNc=False,mode="Console",buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    base_draw(x,y,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)