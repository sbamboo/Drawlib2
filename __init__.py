# Exists to allow relative import

from . import assets
from . import coloring
from . import consoletools
from . import core
from . import dtypes
from . import fonts
from . import generators
from . import imaging
from . import legacy
from . import linedraw
from . import manip
from . import objects
from . import pointGroupAlgorithms
from . import shapes
from . import terminal
from . import tools

from .libs import conUtils as lib_conUtils
from .libs import crshpiptools as lib_crshpiptools
from .libs import stringTags as lib_stringTags

fill_terminal = linedraw.fill_terminal
reset_write_head = terminal.reset_write_head
stdpalette = coloring.DrawlibStdPalette
DrawlibOut = core.DrawlibOut

baseGenerator = generators.baseGenerator
repeatGenerator = generators.repeatGenerator
numberGenerator = generators.numberGenerator
rainbowGenerator = generators.rainbowGenerator
rainbowGeneratorZero = generators.rainbowGeneratorZero

class DrawlibRenderer():
    def __init__(self):
        self.assets = assets
        self.coloring = coloring
        self.consoletools = consoletools
        self.core = core
        self.dtypes = dtypes
        self.fonts = fonts
        self.generators = generators
        self.imaging = imaging
        self.legacy = legacy
        self.linedraw = linedraw
        self.manip = manip
        self.objects = objects
        self.pointGroupAlgorithms = pointGroupAlgorithms
        self.shapes = shapes
        self.terminal = terminal
        self.tools = tools
        
        self.fill_terminal = fill_terminal
        self.stdpalette = stdpalette
        self.reset_write_head = terminal.reset_write_head
        self.DrawlibOut = core.DrawlibOut