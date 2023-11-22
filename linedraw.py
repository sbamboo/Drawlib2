from core import base_draw,base_fill,base_mdraw
from coloring import DrawlibStdPalette
from pointGroupAlgorithms import *
from tools import capIntsX,capIntsY

def move_write_head(x=int,y=int):
    line = "\033[{};{}H".format(x,y)
    print(line)

def fill_terminal(st=str, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    base_fill(st,output,baseColor,palette,drawNc)

def draw_point(st=str,x=int,y=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    base_draw(st,x,y,output,baseColor,palette,drawNc)

def draw_line(st=str,x1=int,y1=int,x2=int,y2=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    coords = beethams_line_algorithm(x1,y1,x2,y2)
    base_mdraw(st,coords,output,baseColor,palette,drawNc)

def draw_triangle_sides(st,s1,s2,s3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    draw_line(st,*s1[0],*s1[1], output,baseColor,palette,drawNc)
    draw_line(st,*s2[0],*s2[1], output,baseColor,palette,drawNc)
    draw_line(st,*s3[0],*s3[1], output,baseColor,palette,drawNc)
def draw_triangle_points(st,p1,p2,p3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    draw_line(st,*p1,*p2, output,baseColor,palette,drawNc)
    draw_line(st,*p1,*p3, output,baseColor,palette,drawNc)
    draw_line(st,*p2,*p3, output,baseColor,palette,drawNc)
def draw_triangle_coords(st,x1,y1,x2,y2,x3,y3, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    p1 = [x1,y1]
    p2 = [x2,y2]
    p3 = [x3,y3]
    draw_line(st,*p1,*p2, output,baseColor,palette,drawNc)
    draw_line(st,*p1,*p3, output,baseColor,palette,drawNc)
    draw_line(st,*p2,*p3, output,baseColor,palette,drawNc)

def draw_circle(st=str,xM=int,yM=int,r=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
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
    base_mdraw(st,coords,output,baseColor,palette,drawNc)

def draw_ellipse(char=str,cX=int,cY=int,xRad=int,yRad=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
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
    base_mdraw(st,coords,output,baseColor,palette,drawNc)

def draw_quadBezier(char,sX=int,sY=int,cX=int,cY=int,eX=int,eY=int, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
    # CapValues
    capIntsX([sX,cX,eX])
    capIntsY([sY,cY,eY])
    # Calculate Coordinates
    coords = generate_quadratic_bezier(sX,sY,cX,cY,eX,eY)
    # Draw coordinates
    base_mdraw(st,coords,output,baseColor,palette,drawNc)

def draw_cubicBezier(char,sX=int,sY=int,c1X=int,c1Y=int,c2X=int,c2Y=int,eX=int,eY=int, algorithm="step",modifier=None, output=object,baseColor=None,palette=DrawlibStdPalette,drawNc=False):
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
    base_mdraw(st,coords,output,baseColor,palette,drawNc)