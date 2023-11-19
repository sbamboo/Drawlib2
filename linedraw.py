from core import base_draw,base_fill,base_mdraw,vw,vh,DrawlibOut
from coloring import DrawlibStdPalette
from pointGroupAlgorithms import beethams_line_algorithm
from tools import *

def move_write_head(x=int,y=int):
    line = "\033[{};{}H".format(x,y)
    print(line)

def fill_terminal(st, baseColor=None,palette=DrawlibStdPalette, wi=None,hi=None,overwWidth=None,overwHeight=None,mode=None,drawNc=False, buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    if wi != None: overwWidth = wi
    if hi != None: overwHeight = hi
    base_fill(st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_point(st,x,y, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    base_draw(x,y,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_line(st,x1,y1,x2,y2, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    coords = beethams_line_algorithm(x1,y1,x2,y2)
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_triangle_sides(st,s1,s2,s3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    # side 1
    draw_line(st,*s1[0],*s1[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    # side 2
    draw_line(st,*s2[0],*s2[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    # side 3
    draw_line(st,*s3[0],*s3[1], baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
# Same but using points
def draw_triangle_points(st,p1,p2,p3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    draw_line(st,*p1,*p2, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p1,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p2,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
# Same but using coords
def draw_triangle_coords(st,x1,y1,x2,y2,x3,y3, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    p1 = [x1,y1]
    p2 = [x2,y2]
    p3 = [x3,y3]
    draw_line(st,*p1,*p2, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p1,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)
    draw_line(st,*p2,*p3, baseColor,palette,overwWidth,overwHeight,drawNc,mode,buffIChar,buffAutoStr,buffInst,channelObj,outputObj)

def draw_circle(st=str,xM=int,yM=int,r=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    rigX = xM+r
    lefX = xM-r
    topY = yM+r
    botY = yM-r
    diam = (r*2)+1
    # CapValues
    capIntsX([xM,rigX,lefX])
    capIntsY([yM,topY,botY])
    # Calculate Coordinates
    coords = beethams_circle_algorithm(xM,yM,r)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_ellipse(char=str,cX=int,cY=int,xRad=int,yRad=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    rigX = cX+xRad
    lefX = cX-xRad
    topY = cY+yRad
    botY = cY-yRad
    # CapValues
    capIntsX([cX,rigX,lefX])
    capIntsY([cY,topY,botY])
    # Calculate Coordinates
    coords = beethams_ellipse_algorithm(cX,cY,xRad,yRad)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_quadBezier(char,sX=int,sY=int,cX=int,cY=int,eX=int,eY=int, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    # CapValues
    capIntsX([sX,cX,eX])
    capIntsY([sY,cY,eY])
    # Calculate Coordinates
    coords = generate_quadratic_bezier(sX,sY,cX,cY,eX,eY)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)

def draw_cubicBezier(char,sX=int,sY=int,c1X=int,c1Y=int,c2X=int,c2Y=int,eX=int,eY=int, algorithm="step",modifier=None, baseColor=None,palette=DrawlibStdPalette, overwWidth=None,overwHeight=None,drawNc=False,mode="Console", buffIChar=" ",buffAutoStr=True,buffInst=None,channelObj=None,outputObj=None):
    '''
    Alogrithm: "step" or "point"
    Modifier: With step algorithm, def: 0.01; With point algorithm, def: 100
    '''
    # CapValues
    capIntsX([sX,c1X,c2X,eX])
    capIntsY([sY,c1Y,c2Y,eY])
    # Calculate Coordinates
    coords = generate_cubic_bezier(sX, sY, c1X, c1Y, c2X, c2Y, eX, eY, algorithm,modifier)
    # Draw coordinates
    base_mdraw(coords,st,overwWidth,overwHeight,mode,drawNc,buffIChar,buffAutoStr,buffInst,channelObj,outputObj,baseColor,palette)