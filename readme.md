# Drawlib

## Drawlib is a simple CLI/TUI drawing library (renderer) made in python.

Author:  Simon Kalmi Claesson
* For version information see lib.json

### Files:
    __init__.py: Contains the renderer wrapper class. (As well as functioning as the package root)
    assets.py: Asset/TextureAsset rendering and handling functions.
    coloring.py: Mostly internal but contains functions and palettes for handling colors and advanced formatting in drawlib.
    consoletools.py: Contains some tools regarding console, for example sizeAssist. (Not to be confused with /libs/conUtils)
    core.py: As the name implies contains the core of drawlib, the Exceptions/Classes and main functionality.
    dtypes.py: Datatype classes for converting and handling data in drawlib.
    fonts.py: Additional tools for font management, requires BeutifulSoup4 and matplotlib.
    generators.py: Contains some character-generators for use with shapeObjects from objects.py (Not to be confused with shapes from /shapes.py)
    imaging.py: Contains classes/wrappers for the imageRenderer functionality of drawlib.
    legacy.py: Contains legacy/broken/deprecated code, no support will be given for anything in here.
    linedraw.py: Contains functions for linedrawing, including some functions for some predefined shapes.
    manip.py: Tools and functions for manipulating texture-data.
    objects.py: Contains some premade shape-classes buidling on drawlibObj, support for character-generators.
    pointGroupAlgorithms.py: Contains raster-algorithms for drawlibs included shapes/linedrawers.
    shapes.py: Contains classes for some premade shapes, building on the linedraw.py implementations. (No support for character-generators)
    terminal.py: The most basic core functionality of drawlib, its building-blocks live here. Some basic ANSI rendering functions.
    tools.py: Contains some tools for internal use in drawlib aswell as use by the users.

### Difference between objects.py and shapes.py
As noted above objects.py and shapes.py are very similar, except classes from objects.py support character-generators.

The classes in objects.py are based of the datatypes, more specifically splitPixelGroup.
Thus allowing for more use cases.

The classes in shapes.py are instead building directly of the linedrawer functions and exists more to halfly "object-orient" the linedrawer functions.

*They are kept in their own file since merging with linedraw.py would make it even harder to understand the difference. (In my opinion)*

### Examples:
#### Class Import
```
from Drawlib2 import DrawlibRenderer
renderer = DrawlibRenderer()

renderer.fill_terminal(" ")
renderer.objects.circleObj("#",20,20,7,"f_red",renderer.stdpalette).draw()
renderer.basicShapes.circle("#",30,20,7,"f_blue",renderer.stdpalette).draw()
renderer.objects.pointObj("#",10,10,"f_magenta",renderer.stdpalette).draw()
renderer.objects.ellipseObj("#",70,15,15,5,"f_yellow",renderer.stdpalette).draw()
renderer.objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",renderer.stdpalette).draw()
renderer.objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```

#### As Import
```
import drawlib as renderer

renderer.fill_terminal(" ")
renderer.objects.circleObj("#",20,20,7,"f_red",renderer.stdpalette).draw()
renderer.basicShapes.circle("#",30,20,7,"f_blue",renderer.stdpalette).draw()
renderer.objects.pointObj("#",10,10,"f_magenta",renderer.stdpalette).draw()
renderer.objects.ellipseObj("#",70,15,15,5,"f_yellow",renderer.stdpalette).draw()
renderer.objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",renderer.stdpalette).draw()
renderer.objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```

#### Star Import
```
from drawlib import *

fill_terminal(" ")
objects.circleObj("#",20,20,7,"f_red",stdpalette).draw()
basicShapes.circle("#",30,20,7,"f_blue",stdpalette).draw()
objects.pointObj("#",10,10,"f_magenta",stdpalette).draw()
objects.ellipseObj("#",70,15,15,5,"f_yellow",stdpalette).draw()
objects.quadBezierObj("#",30,30,0,0,50,0,"f_darkred",stdpalette).draw()
objects.cubicBezierObj("#",30,20,30,0,70,0,70,20).draw()
```