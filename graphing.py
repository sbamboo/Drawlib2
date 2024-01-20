import re
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, lambdify

def parse_function_string(function_string):
    # Using regular expression to parse the function string
    match = re.match(r'^(\w)\((\w)\)\s*=\s*(.+)$', function_string)
    
    if match:
        func_char, var, equation = match.groups()
        return func_char, var, equation
    else:
        raise ValueError("Invalid function string format. Example format: f(x) = x**2")

def plot_function(function_string, x_range=(-10, 10), y_range=None, show_plot=False):
    func_char, var, equation = parse_function_string(function_string)

    # Create a symbolic variable
    x = symbols(var)

    # Convert the equation to a symbolic expression
    expr = eval(equation)

    # Lambdify the expression for numerical evaluation
    func = lambdify(x, expr, 'numpy')

    # Create a list of tuples for each integer point within the specified ranges
    points_list = [(int(x), max(min(int(func(x)), int(y_range[1])), int(y_range[0]))) for x in range(int(x_range[0]), int(x_range[1]) + 1)]

    # Display the plot if show_plot is True
    if show_plot:
        x_values = np.linspace(x_range[0], x_range[1], 1000)
        y_values = func(x_values)

        plt.plot(x_values, y_values, label=f'{func_char}({var})={equation}')
        plt.scatter(*zip(*points_list), color='red', label='Integer Points')
        plt.xlabel(var)
        plt.ylabel(f'{func_char}({var})')
        plt.xticks(np.arange(int(x_range[0]), int(x_range[1]) + 1, 1))
        
        if y_range is not None:
            plt.yticks(np.arange(int(y_range[0]), int(y_range[1]) + 1, 1))
        
        plt.legend()
        plt.grid(True)
        plt.title(f'Graph of {func_char}({var})={equation}')
        
        # Set limits for x and y axes
        plt.xlim(x_range)
        if y_range is not None:
            plt.ylim(y_range)

        plt.show()

    return points_list

# Example usage:
function_string = "f(x) = x**2"
x_range = (-10, 10)
y_range = (-10, 10)  # Adjust the y-range as needed
result = plot_function(function_string, x_range=x_range, y_range=y_range, show_plot=True)

# Print the list of tuples
print(result)
