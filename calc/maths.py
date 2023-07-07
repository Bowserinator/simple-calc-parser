import cmath as math
from functools import reduce
import operator

import calc.vector as vector

class Function(object):
    def __init__(self, f, argc):
        """
        :param f: Function to call, (a, b, c...) -> num or other
        :param argc: Number of arguments the function takes
        """
        self.argc = argc
        self.f = f

    def __call__(self, args):
        if len(args) == 1 and isinstance(args[0], vector.Vector):
            # If there is only 1 vector argument, and the function takes
            # a single argument, the function is applied to every element
            # of the argument, ie sin([0, 1]) -> [sin(0), sin(1)]
            if self.argc == 1:
                return vector.Vector([self.f([x]) for x in args[0]])
            
            # If there is only one vector argument, and the function is vararg, the vector
            # is taken to be the args to the function
            if self.argc == -1:
                return self.f(args[0].items)

        return self.f(args)


def _angle(args):
    """Angle between two vectors"""
    a, b = args
    return math.acos(a.dot(b) / (abs(a) * abs(b)))

def _angle3(args):
    """Solve for angle between 3 points expressed as vectors"""
    a, center, b = args
    return _angle([a - center, b - center])

FUNCTIONS = {
    "sin": Function(lambda args: math.sin(args[0]), 1),
    "cos": Function(lambda args: math.cos(args[0]), 1),
    "tan": Function(lambda args: math.tan(args[0]), 1),
    "asin": Function(lambda args: math.asin(args[0]), 1),
    "acos": Function(lambda args: math.acos(args[0]), 1),
    "atan": Function(lambda args: math.atan(args[0]), 1),
    "atan2": Function(lambda args: math.atan2(args[0], args[1]), 2),
    "degrees": Function(lambda args: math.degrees(args[0]), 1),
    "radians": Function(lambda args: math.radians(args[0]), 1),

    "abs": Function(lambda args: math.sqrt(sum([abs(x ** 2) for x in args])), -1),
    "ceil": Function(lambda args: math.ceil(args[0]), 1),
    "floor": Function(lambda args: math.floor(args[0]), 1),
    "gcd": Function(lambda args: math.gcd(args[0], args[1]), 2),
    "lcm": Function(lambda args: math.lcm(args[0], args[1]), 2),
    "sqrt": Function(lambda args: math.sqrt(args[0]), 1),
    "cbrt": Function(lambda args: math.cbrt(args[0]), 1),

    "exp": Function(lambda args: math.e ** (args[0]), 1),
    "exp2": Function(lambda args: 2 ** (args[0]), 1),
    "log": Function(lambda args: math.log(args[0]), 1),
    "ln": Function(lambda args: math.log(args[0]), 1),
    "log2": Function(lambda args: math.log2(args[0]), 1),
    "lg": Function(lambda args: math.log2(args[0]), 1),
    "log10": Function(lambda args: math.log10(args[0]), 1),
    "modpow": Function(lambda args: pow(args[0], args[1], args[2]), 1),

    "max": Function(lambda args: max(args), -1),
    "min": Function(lambda args: min(args), -1),
    "sum": Function(lambda args: sum(args), -1),
    "prod": Function(lambda args: reduce(operator.mul, args, 1), -1),

    # Vector functions
    "angle": Function(_angle, 2),
    "angle3": Function(_angle3, 3),
    "sort": Function(lambda args: vector.Vector(sorted(args)), -1),
    "rsort": Function(lambda args: vector.Vector(sorted(args, reverse=True)), -1),
    "len": Function(lambda args: len(args), -1)
}

CONSTANTS = {
    # Math constants
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + (5) ** 0.5) / 2,
    "i": (-1) ** 0.5,
    "j": (-1) ** 0.5,
    "sqrt2": 2 ** 0.5,
    
    # Minecraft constants
    "shulker": 1728,
    "stack": 64,
    "dub": 1728 * 2
}

BIN_OPS = {
    "**": lambda a, b: a ** b,
    "^": lambda a, b: a ** b,
    "//": lambda a, b: a // b,
    "/": lambda a, b: a / b,
    "*": lambda a, b: a * b,
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "%": lambda a, b: a % b
}
BIN_OPS_PRECEDENCE = { "**": 10, "^": 10, "//": 9, "/": 9, "*": 9, "+": 8, "-": 8, "%": 7 }
