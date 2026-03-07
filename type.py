"""Implements functions for type reading, hierarchy, and conversion"""

from bit import Bit
from unsigned import Unsigned


def typeof(x):
    # Return a string representing the type and bit size of x
    tx = type(x)
    if tx is type(Bit()):
        return "B1"
    elif tx is type(Unsigned()):
        return f"U{len(x)}"
    else: # x is some other Python type
        return str(tx)


def highest(x, y):
    # Return the narrowest type that can represent both x and y
    tx, ty = typeof(x), typeof(y)
    if tx is ty:
        return tx
    elif tx[0] is 'B' or ty[0] is 'B':
        return tx if tx[0] is not 'B' else ty
    elif tx[0] is 'U' and ty[0] is 'U':
        return f"U{max(typeof(x))}"
    else: # Unknown hierarchy for x and y
        raise TypeError(
            f"highest function failed for types {tx!s} and {ty!s}"
        )


def convert(x, t):
    pass


def promote(a, b):
    # Return a and b promoted as needed to be the same type
    if typeof(a) is typeof(b):
        return a, b
    elif typeof(a) is "B1" or typeof(b) is "B1":
