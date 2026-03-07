"""Implements a simple class to represent a single hardware bit (0 or 1)"""

# Randrange for randomizing uninitialized bits
from random import randrange as _random_randrange


# The bit class itself

class Bit:
    """Straightforward class representing a single hardware bit (0 or 1)."""

    # Class constuctor

    def __init__(self, state=None):
        """Create a new bit, optionally initializing its value."""

        # Randomize an uninitialized bit (just like real life!)
        if state is None:
            # Note that range(2) = [0, 1]
            state = _random_randrange(2)

        # Convert the state to bool just in case
        self._state = bool(state)

    # Representation methods

    def __repr__(self):
        """Produce a Python representation, either Bit(False) or Bit(True)."""

        # Substitute the state into a constuctor call string
        return f"{self.__class__.__name__}({self._state!r})"

    def __str__(self):
        """Print 0 or 1 to serve as an expression of the bit's value."""

        # Pick a return value with a one-line conditional statement
        return "1" if self._state else "0"

    # Comparison methods

    def __lt__(self, other):
        """Return whether self < other."""

        _bit_check(other)
        # This is only true if self is 0 and other is 1
        return not self._state and other._state

    def __le__(self, other):
        """Return whether self <= other."""

        _bit_check(other)
        # This is only false if self is 1 and other is 0
        return not self._state or other._state

    def __eq__(self, other):
        """Return whether self == other."""

        _bit_check(other)
        # Sufficient to check that their states are equal
        return self._state == other._state

    def __ne__(self, other):
        """Return whether self != other."""

        _bit_check(other)
        # Sufficient to check that their states are unequal
        return self._state != other._state

    def __gt__(self, other):
        """Return whether self > other."""

        _bit_check(other)
        # This is only true if self is 1 and other is 0
        return (self._state and not other._state)

    def __ge__(self, other):
        """Return whether self >= other."""

        _bit_check(other)
        # This is only false if self is 0 and other is 1
        return (self._state or not other._state)

    # Boolean evaluation method

    def __bool__(self):
        """Converts a bit to a bool and makes Bit(Bit()) work properly."""

        # Just give the value of the bit's state
        return self._state

    # Bitwise operator methods

    def __and__(self, other):
        """Implements bitwise and using the & operator."""

        _bit_check(other)
        # Evaluate using logical and on their bit states
        return Bit(self._state and other._state)

    def __xor__(self, other):
        """Implements bitwise xor using the ^ operator."""

        _bit_check(other)
        # Xor is equivalent to asking whether the bits' states are unequal
        return Bit(self._state != other._state)

    def __or__(self, other):
        """Implements bitwise or using the | operator."""

        _bit_check(other)
        # Evaluate using logical or on their bit states
        return Bit(self._state or other._state)

    # Reflected bitwise operator methods

    def __rand__(self, other):
        """Implements & from the right side."""

        _bit_check(other)
        # Check will probably fail in this situation, but just in case...
        # ...commute the two operands and invoke the code for __and__
        return self & other

    def __rxor__(self, other):
        """Implements ^ from the right side."""

        _bit_check(other)
        # Check will probably fail in this situation, but just in case...
        # ...commute the two operands and invoke the code for __xor__
        return self ^ other

    def __ror__(self, other):
        """Implements | from the right side."""

        _bit_check(other)
        # Check will probably fail in this situation, but just in case...
        # ...commute the two operands and invoke the code for __or__
        return self | other

    # Augmented assignment bitwise operator methods

    def __iand__(self, other):
        """Implements augmented assignment with the &= operator."""

        # Invoke the code for __and__ to avoid code duplication
        return self & other

    def __ixor__(self, other):
        """Implements augmented assignment with the ^= operator."""

        # Invoke the code for __xor__ to avoid code duplication
        return self ^ other

    def __ior__(self, other):
        """Implements augmented assignment with the |= operator."""

        # Invoke the code for __or__ to avoid code duplication
        return self | other

    # Unary bitwise not method

    def __invert__(self):
        """Implements bitwise not using the unary ~ operator."""

        return Bit(not self._state)


# Bit type checking function

def _bit_check(obj):
    """Check that obj is a bit object and raise an error if it is not."""

    if not isinstance(obj, Bit):
        raise TypeError("bit operands must be bit objects")


# Bit "literals"

ZERO = Bit(False)
ONE = Bit(True)


# Code for testing the bit class

if __name__ == "__main__":

    # Print message for user
    print("Testing bit class...")

    # Test the state initialization
    print("  Testing state initialization")
    assert Bit(False) == ZERO
    assert Bit(True) == ONE
    assert Bit(0) == ZERO
    assert Bit(1) == ONE
    assert Bit(ZERO) == ZERO
    assert Bit(ONE) == ONE
    assert Bit(0.0) == ZERO
    assert Bit(1.0) == ONE

    # Test the random initialization
    print("  Testing random initialization")
    N_SAMPLES = 10 ** 6
    bits = [Bit() for _ in range(N_SAMPLES)]
    mean = sum((1 if b == ONE else 0) for b in bits) / float(N_SAMPLES)
    assert 0.45 < mean < 0.55

    # Test the string representations
    print("  Testing representations")
    assert repr(ZERO) == "Bit(False)"
    assert repr(ONE) == "Bit(True)"
    assert str(ZERO) == "0"
    assert str(ONE) == "1"

    # Test the comparison operators
    print("  Testing comparisons")
    for x1 in range(2):
        for x2 in range(2):
            b1 = Bit(x1)
            b2 = Bit(x2)
            assert (b1 < b2) == (x1 < x2)
            assert (b1 <= b2) == (x1 <= x2)
            assert (b1 == b2) == (x1 == x2)
            assert (b1 != b2) == (x1 != x2)
            assert (b1 > b2) == (x1 > x2)
            assert (b1 >= b2) == (x1 >= x2)

    # Test the conversion to bool
    print("  Testing bool")
    assert bool(ZERO) is False
    assert bool(ONE) is True

    # Test the bitwise operators
    print("  Testing bitwise operators")
    for x1 in range(2):
        for x2 in range(2):
            b1 = Bit(x1)
            b2 = Bit(x2)
            assert str(b1 & b2) == str(x1 & x2)
            assert str(b1 ^ b2) == str(x1 ^ x2)
            assert str(b1 | b2) == str(x1 | x2)

    # Test the bitwise not operator
    print("  Testing bitwise not")
    assert ~ZERO == ONE
    assert ~ONE == ZERO

    # Test the bit check function
    print("  Testing bit check function")
    for o in [1, 1.0, 1.0+1.0j, "a", [], tuple(), {}, True]:
        error = False
        try:
            _bit_check(o)
        except TypeError:
            error = True
        assert error

    # Print closing message
    print("All tests passed!")
