Needs:
1. Generating to an internal datatype or to an output, an output is a buffer or the console-connector.
2. Console-connector must be able to consecutivly print to console at x,y without issues.

Outputs:
  Outputs like the drawlib_buffer or drawlib_console (console-connector), should have both char and string methods.
  Char method:
    X,Y,Char  Places a char at given x,y

  String method:
    X,Y,String Places a string starting at given x,y

General rules:
1. Al coorinates must originate by shape/objects (x:0,y:0 = TopLeft)
*Moved to objectiveCLI project

OrginPoint:
  This function can offset the origin-point of a shape/object.
  It takes X,Y,Origin
  Where origin can be: TL,TR,BL,BR,Center,Top,Left,Right,Bottom,{offX,offY}
  A instance of the orgin-point handler of any ab
*Moved to objectiveCLI project