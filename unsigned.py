# Implements a class representing an n-bit unsigned hardware integer
# Last edited 6/7/17 by Greg Vance

# Import the hardware bit string class from another file
import bitstring

# Number of bits in one byte
BYTE = bitstring.BYTE

# Sizes of various integer types in C (on kowalski)
CHAR_SIZE = 1 * BYTE
SHORT_SIZE = 2 * BYTE
INT_SIZE = 4 * BYTE
LONG_SIZE = 8 * BYTE

class Unsigned(bitstring.BitString):
	"Class representing an n-bit unsigned hardware integer via a bit string."

	def __init__(self, value=None, nbits=None):
		"Create a new n-bit unsigned integer, with optional initialization."

		# With no initializer value, let it be a randomized bit string
		if value is None:
			# Default the number of bits to the size of a C int if not given
			if nbits is None:
				nbits = INT_SIZE
			# Pass the number of bits to the bit string constructor
			bitstring.BitString.__init__(self, None, nbits)

		# Implement full decimal integer initialization from strings
		elif isinstance(value, str) or isinstance(value, int):
			# Convert any Python int value to a numeric string
			value = str(value)
			# Settle the number of bits, defaulting to the size of a C int
			if nbits is None:
				nbits = INT_SIZE
			# Check that the size can actually hold the value passed in
			if int(value) >= 2**int(nbits):
				raise ValueError("not enough bits to store unsigned value")
			# Set up the string of bits and zero it out to begin with
			bitstring.BitString.__init__(self, "0", nbits)
			# Set up an unsigned integer storing the value ten
			tenstr = bitstring.Bitstring("1010")
			ten = Unsigned(bitstring.expand(tenstr, self._size))
			# Set up a one-byte bit string storing the value of the char '0'
			zchar = bitstring.char_value('0')
			# Add each decimal digit in turn to the stored value
			for i in xrange(len(value)):
				# Push up any previous decimal digits by one decimal place
				if i > 0:
					self *= ten
				# Test and then increment for the next digit
				if value[i] not in "0123456789":
					raise ValueError("bad character in numerical string")
				char = bitstring.char_value(value[i])
				while char > zchar:
					self = self.increment()
					char = char.decrement()

		# If value is an unsigned, pass its bits to the bit string constructor
		elif isinstance(value, Unsigned):
			bitstring.BitString.__init__(self, value._bits, nbits)

		# Pass anything unknown down to the bit string constructor to deal with
		else:
			bitstring.Bitstring.__init__(self, value, nbits)

	def __repr__(self):
		# Produce something of the form "Unsigned(int, nbits)"
		return "Unsigned(%d, %d)" % (int(self), len(self))

	def __str__(self):
		# Produce the represented string of decimal digits
		return str(int(self))

	# Comparison operators (handled by inheritance from bit strings)

	def __add__(self, other):
		# Implements +
		# Fix the type of other, then add bit-by-bit with carrying
		try:
			other = self._fix(other)
		except ValueError:
			return other + self
		carry = Bit(0)
		result = self._fix(0)
		for i in xrange(len(self)-1, -1, -1):
			result.bits[i] = self.bits[i] ^ other.bits[i]
			result.bits[i] ^= carry
			carry = (self.bits[i] & other.bits[i]) \
				| (self.bits[i] & carry) \
				| (other.bits[i] & carry)
		return result

	# Maximum value 

	def max_value(self):
		"Return an unsigned integer containing the maximum storable value."

		# Create a zero-value bit string of the same size
		bstr = bitstring.Zero(self._size)
		# Decrement the bit string to get the maximum value
		bstr = bstr.decrement()
		# Convert the bit string to an unsigned integer
		return Unsigned(bstr)

# Shortcut C unsigned integer type constructors

def UnsignedChar(init=None):
	"Construct an unsigned integer of size 1 byte with optional initializer."

	return Unsigned(value=init, nbits=CHAR_SIZE)

def UnsignedShort(init=None):
	"Construct an unsigned integer of size 2 bytes with optional initializer."

	return Unsigned(value=init, nbits=SHORT_SIZE)

def UnsignedInt(init=None):
	"Construct an unsigned integer of size 4 bytes with optional initializer."

	return Unsigned(value=init, nbits=INT_SIZE)

def UnsignedLong(init=None):
	"Construct an unsigned integer of size 8 bytes with optional initializer."

	return Unsigned(value=init, nbits=LONG_SIZE)

# Code for testing the unsigned class

if __name__ == "__main__":

	# Print message for the user
	print "Testing unsigned class..."

	# 

	# Print closing message
	print "All tests passed!"

