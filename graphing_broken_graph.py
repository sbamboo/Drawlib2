import re
import numpy as np
from sympy import symbols, lambdify
import matplotlib.pyplot as plt

def parse_function_string(function_string):
    # Using regular expression to parse the function string
    match = re.match(r'^(\w)\((\w)\)\s*=\s*(.+)$', function_string)
    
    if match:
        func_char, var, equation = match.groups()
        return func_char, var, equation
    else:
        raise ValueError("Invalid function string format. Example format: f(x) = x**2")

def plot_function(function_string, x_range=(-10, 10), y_range=None, x_step=1.0, y_step=1.0, floatRndDecis=2, intScale=False, intScaleRound=False, display_plot=False):
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
    if intScale:
        # Determine the appropriate multiplier for each axis
        x_multiplier = int(1 / x_step) if x_step.is_integer() else int(1 / (x_step % 1))
        y_multiplier = int(1 / y_step) if y_step.is_integer() else int(1 / (y_step % 1))
        # Scale and if enabled round to ints
        if intScaleRound:
            points_list = [(round(x_val * x_multiplier), round(y_val * y_multiplier)) for x_val, y_val in points_list]
        else:
            points_list = [(x_val * x_multiplier, y_val * y_multiplier) for x_val, y_val in points_list]

    if display_plot:
        x_vals = np.arange(x_range[0], x_range[1] + x_step, x_step)
        y_vals = func(x_vals)

        plt.plot(x_vals, y_vals)
        plt.xlabel(var)
        plt.ylabel(func_char + "(" + var + ")")
        plt.title("Plot of " + function_string)

        # Set the tick positions and labels based on the specified step variables
        x_ticks = np.arange(x_range[0], x_range[1] + x_step, x_step)
        y_ticks = np.arange(y_range[0], y_range[1] + y_step, y_step) if y_range is not None else None

        plt.xticks(x_ticks)
        plt.yticks(y_ticks)

        # Set the plot limits to match the specified ranges
        plt.xlim(x_range[0], x_range[1])
        if y_range is not None:
            plt.ylim(y_range[0], y_range[1])

        # Remove grid lines
        plt.grid(False)

        plt.show()

    return points_list

# Example usage:
function_string = "f(x) = x**2"
x_range = (-10, 10)
y_range = (-10, 10)
x_step = 1.0
y_step = 1.0
floatRndDecis = 2
intScale = True
intScaleRound = True
display_plot = True
result = plot_function(function_string, x_range=x_range, y_range=y_range, x_step=x_step, y_step=y_step, floatRndDecis=floatRndDecis, intScale=intScale, intScaleRound=intScaleRound, display_plot=display_plot)

# Print the list of tuples
print(result)
