import re
import numpy as np
from sympy import symbols, lambdify
import matplotlib.pyplot as plt

from .pointGroupAlgorithms import beethams_line_algorithm

def parse_function_string(function_string):
    # Using regular expression to parse the function string
    match = re.match(r'^(\w)\((\w)\)\s*=\s*(.+)$', function_string)
    
    if match:
        func_char, var, equation = match.groups()
        return func_char, var, equation
    else:
        raise ValueError("Invalid function string format. Example format: f(x) = x**2")

def plot_function(function_string, x_range=(-10, 10), y_range=None, x_step=1.0, y_step=1.0, floatRndDecis=2, intScale=False, intScaleRound=False, display_plot=False, debugGrid=False):
    func_char, var, equation = parse_function_string(function_string)

    # Create a symbolic variable
    x = symbols(var)

    # Convert the equation to a symbolic expression
    expr = eval(equation)

    # Lambdify the expression for numerical evaluation
    func = lambdify(x, expr, 'numpy')

    # Adjust the step size based on the scale
    x_step = x_step if x_step > 0 else 1.0
    y_step = y_step if y_step > 0 else 1.0

    # Create a list of tuples for each scaled point within the specified ranges
    points_list = [
        (round(x_val, floatRndDecis), round(func(x_val) * y_step, floatRndDecis)) 
        for x_val in np.arange(x_range[0], x_range[1] + x_step, x_step)
        if y_range is None or (y_range[0] <= func(x_val) * y_step <= y_range[1])
    ]

    # Multiply the values by a calculated scale factor to ensure ints
    floatPoints = points_list.copy()
    if intScale:
        # Determine the appropriate multiplier for each axis
        x_multiplier = int(1 / x_step) if float(x_step).is_integer() else int(1 / (x_step % 1))
        y_multiplier = int(1 / y_step) if float(y_step).is_integer() else int(1 / (y_step % 1))
        # Scale and if enabled round to ints
        points_list = [(x_val * x_multiplier, y_val * y_multiplier) for x_val, y_val in points_list]
        floatPoints = points_list.copy() #update
        if intScaleRound:
            points_list = [(round(x_val), round(y_val)) for x_val, y_val in points_list]

    if display_plot:
        x_values = np.linspace(x_range[0], x_range[1], 1000)
        y_values = func(x_values)

        xstepFactor = x_step if x_step < 0 else 1
        ystepFactor = y_step if y_step < 0 else 1
        pointValues = [(xval*xstepFactor, yval*ystepFactor) for xval,yval in floatPoints]

        plt.plot(x_values, y_values, label=f'{func_char}({var})={equation}')
        plt.scatter(*zip(*pointValues), color='red', label='Integer Points')
        plt.xlabel(var)
        plt.ylabel(f'{func_char}({var})')
        plt.xticks(np.arange(int(x_range[0]), int(x_range[1]) + 1, 1))
        
        if y_range is not None:
            plt.yticks(np.arange(int(y_range[0]), int(y_range[1]) + 1, 1))
        
        plt.legend()
        plt.grid(debugGrid)
        plt.title(f'Graph of {func_char}({var})={equation}')
        
        # Set limits for x and y axes
        plt.xlim(x_range)
        if y_range is not None:
            plt.ylim(y_range)

        plt.show()

    return {"positions":points_list,"data":floatPoints}

class AttemptedOperationOnUnplottedGraph(Exception):
    def __init__(self,message="Drawlib.Graphing: Attempted method on unplotted grap, use .plot(...) first!"):
        self.message = message
        super().__init__(self.message)

class graphPlotter():
    def __init__(self,function,output=object,pointChar="X",fillChar="*"):
        self.function = function
        self.output = output
        self.pointChar = pointChar
        self.fillChar = fillChar
        self.data = None

    def _getTopMost(self,positions) -> int:
        topMostFound = None
        for pos in positions:
            if topMostFound == None:
                topMostFound = pos[1]
            else:
                if pos[1] < topMostFound:
                    topMostFound = pos[1]
        return topMostFound
    def _getLeftMost(self,positions) -> int:
        topLeftFound = None
        for pos in positions:
            if topLeftFound == None:
                topLeftFound = pos[0]
            else:
                if pos[0] < topLeftFound:
                    topLeftFound = pos[0]
        return topLeftFound
    
    def _invertY(self,positions):
        newPositions = []
        for pos in positions:
            yDiff = 0 + pos[1]
            newPositions.append( (pos[0],pos[1]-(yDiff*2)) )
        return newPositions
    
    def _changeToDispCoords(self,reff=(0,0),positions=list):
        positions = self._invertY(positions)
        leftMost = self._getLeftMost(positions)
        topMost = self._getTopMost(positions)
        xDiff = reff[0]+1 - leftMost
        yDiff = reff[1]+1 - topMost
        newPositions = []
        for pos in positions:
            newPositions.append( (pos[0]+xDiff,pos[1]+yDiff) )
        return newPositions
    
    def plot(self,pos=(0,0),xrange=(-10,10),yrange=(-10,10),xstep=1.0,ystep=1.0,floatRndDecis=2,intScale=True,intScaleRound=True,assumptionFill=False,debug=False,debugGrid=True):
        self.data = plot_function(self.function,x_range=xrange,y_range=yrange,x_step=xstep,y_step=ystep,floatRndDecis=floatRndDecis,intScale=intScale,intScaleRound=intScaleRound,display_plot=debug,debugGrid=debugGrid)
        self.data["pixels"] = self._changeToDispCoords(pos,self.data["positions"])
        self.data["fillPixels"] = []
        if assumptionFill == True:
            pixels = self.data["pixels"]
            for ii in range(0,len(pixels)):
               i = ii-1
               if i >= 0:
                p1 = pixels[i]
                p2 = pixels[ii]
                self.data["fillPixels"].extend( beethams_line_algorithm(*p1,*p2) )
            
    def put(self):
        if self.data == None: raise AttemptedOperationOnUnplottedGraph()
        if self.data["fillPixels"] != []:
            self.output.mPut(self.data["fillPixels"],self.fillChar)
        self.output.mPut(self.data["pixels"],self.pointChar)

    def getValForPx(self,pixel=tuple):
        if self.data == None: raise AttemptedOperationOnUnplottedGraph()
        index = self.data["pixels"].index(pixel)
        return self.data["data"][index]
