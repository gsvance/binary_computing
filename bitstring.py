# Implements a class to represent a string of hardware bits with operations
# Last edited 6/7/17 by Greg Vance

# Import the hardware bit class from another file
import bit

# Number of bits in one byte
BYTE = 8

class BitString:
	"Class representing a string of several hardware bits in computer memory."

	# Class constructor

	def __init__(self, binary=None, size=None):
		"Make a bit string, with optional binary string and number of bits."

		# Use tuples for storing the bits; lists are mutable and cause problems

		# If the binary initializer is already a bit string, extract its data
		if isinstance(binary, BitString):
			binary = binary._bits

		# If no binary initialization is given, store a random string of bits
		if binary is None:
			# If no size is given, default to a size of one 8-bit byte
			if size is None:
				size = BYTE
			# Convert the size to an integer just in case, and check it
			self._size = int(size)
			if self._size <= 0:
				raise ValueError("bit string size must be a positive number")
			# Generate a tuple of uninitialized bits to store
			self._bits = tuple(bit.Bit() for i in xrange(self._size))

		# If a binary string is given, use its digits for initialization
		elif isinstance(binary, str):
			# Permit whitespace in the binary string, but remove it now
			binary = "".join(binary.strip().split())
			# If no size is given, use the string's length for the size
			if size is None:
				size = len(binary) if len(binary) > 0 else 1
			# Convert size to an integer just in case, and double check it
			self._size = int(size)
			if self._size < len(binary):
				raise ValueError("bit string size too small for given value")
			# Store the binary digits in the form of bit objects
			self._bits = []
			for i in xrange(len(binary)):
				# Make sure every character of the string is parseable
				if binary[i] in ('0', '1'):
					self._bits.append(bit.Bit(binary[i] == '1'))
				else:
					raise ValueError("bad character found in binary string")
			# Add any leading zeros needed to complete the data storage
			zeros = self._size - len(self._bits)
			self._bits = tuple([bit.Zero for i in xrange(zeros)] + self._bits)

		# If the the binary initializer is a tuple of bits, then use them
		elif isinstance(binary, tuple) and \
			all([isinstance(b, bit.Bit) for b in binary]):
			# Check and settle the size parameter
			if size is None:
				size = len(binary) if len(binary) > 0 else 1
			self._size = int(size)
			if self._size < len(binary):
				raise ValueError("given bits tuple will not fit in given size")
			# Store the bits with any necessary leading zeros
			zeros = self._size - len(binary)
			self._bits = tuple([bit.Zero for i in xrange(zeros)]) + binary

		# Whatever the binary initializer is, we don't know how to handle it
		else:
			raise TypeError("bit string binary initializer is not usable")

	# Representation methods

	def __repr__(self):
		"Produce a representation of a bit string using Python syntax."

		# Produce a constructor call with the string and size parameters
		return "BitString(\"%s\", %d)" % (string_bits(self), self._size)

	def __str__(self):
		"Print a spaced array of the binary data stored in a bit string."

		# Add in spaces to make the printed array legible
		spacing = 4
		# Append every digit to a list of digits, with spaces as needed
		digit_list = []
		for i in xrange(self._size):
			# Add a space if it is time, put odd remainder digits at the left 
			if (self._size - i) % spacing == 0 and i > 0:
				digit_list.append(' ')
			# Append the next binary digit to the list
			digit_list.append(str(self._bits[i]))
		return "[ %s ]" % ("".join(digit_list))

	# Comparison methods

	def __lt__(self, other):
		"Compare bit string values and return whether self < other."

		_bitstring_check(other, self._size)
		# Check each digit in turn, starting with the largest
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return self._bits[i] < other._bits[i]
		# No digits differed, the bit strings are equal in value
		return False

	def __le__(self, other):
		"Compare bit string values and return whether self <= other."

		_bitstring_check(other, self._size)
		# Check each digit in turn, starting with the largest
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return self._bits[i] < other._bits[i]
		# No digits differed, the bit strings are equal in value
		return True

	def __eq__(self, other):
		"Compare bit string values and return whether self == other."

		_bitstring_check(other, self._size)
		# Check each digit in turn for equality
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return False
		# No digits differed, the bit strings are equal in value
		return True

	def __ne__(self, other):
		"Compare bit string values and return whether self != other."

		_bitstring_check(other, self._size)
		# Check each digit in turn for equality
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return True
		# No digits differed, the bit strings are equal in value
		return False

	def __gt__(self, other):
		"Compare bit string values and return whether self > other."

		_bitstring_check(other, self._size)
		# Check each digit in turn, starting with the largest
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return self._bits[i] > other._bits[i]
		# No digits differed, the bit strings are equal in value
		return False

	def __ge__(self, other):
		"Compare bit string values and return whether self >= other."

		_bitstring_check(other, self._size)
		# Check each digit in turn, starting with the largest
		for i in xrange(self._size):
			if self._bits[i] != other._bits[i]:
				return self._bits[i] > other._bits[i]
		# No digits differed, the bit strings are equal in value
		return True

	# Boolean evaluation method

	def __nonzero__(self):
		"Return False if all stored bits are zero and True otherwise."

		# Check each bit to see if it is nonzero
		for i in xrange(self._size):
			if self._bits[i] == bit.One:
				return True
		# All of the bits were zero
		return False

	# Bitwise operator methods

	def __lshift__(self, other):
		"Shift bits to the left other times, using the << operator."

		_bitstring_check(other)
		# Make a list to store the shifted bits
		shift_bits = [b for b in self._bits]
		# Shift self's bits until other has been decremented to zero
		zero = Zero(other._size)
		while other > zero:
			# Carry out the left shift operation
			for i in xrange(self._size):
				if i + 1 < self._size:
					shift_bits[i] = shift_bits[i + 1]
				# Zeros shift in from the right
				else:
					shift_bits[i] = bit.Zero
			# Decrement the shift counter
			other = other.decrement()
		# Return the shifted result
		return BitString(tuple(shift_bits))

	def __rshift__(self, other):
		"Shift bits to the right other times, using the >> operator."

		_bitstring_check(other)
		# Make a list to store the shifted bits
		shift_bits = [b for b in self._bits]
		# Shift self's bits until other has been decremented to zero
		zero = Zero(other._size)
		while other > zero:
			# Carry out the right shift operation
			for i in xrange(self._size - 1, -1, -1):
				if i > 0:
					shift_bits[i] = shift_bits[i - 1]
				# Zeros shift in from the left
				else:
					shift_bits[i] = bit.Zero
			# Decrement the shift counter
			other = other.decrement()
		# Return the shifted result
		return BitString(tuple(shift_bits))

	def __and__(self, other):
		"The bitwise and of two bit strings, using the & operator."

		_bitstring_check(other, self._size)
		# Create a list of bits for a new bit string to store the result
		result_bits = []
		# Fill each digit of the result
		for i in xrange(self._size):
			result_bits.append(self._bits[i] & other._bits[i])
		# Return the result when all digits have been filled in
		return BitString(tuple(result_bits))

	def __xor__(self, other):
		"The bitwise xor of two bit strings, using the ^ operator."

		_bitstring_check(other, self._size)
		# Create a list of bits for a new bit string to store the result
		result_bits = []
		# Fill each digit of the result
		for i in xrange(self._size):
			result_bits.append(self._bits[i] ^ other._bits[i])
		# Return the result when all digits have been filled in
		return BitString(tuple(result_bits))

	def __or__(self, other):
		"The bitwise or of two bit strings, using the | operator."

		_bitstring_check(other, self._size)
		# Create a list of bits for a new bit string to store the result
		result_bits = []
		# Fill each digit of the result
		for i in xrange(self._size):
			result_bits.append(self._bits[i] | other._bits[i])
		# Return the result when all digits have been filled in
		return BitString(tuple(result_bits))

	# Reflected bitwise operator methods

	def __rlshift__(self, other):
		"Implement the << left shift operation from the right side."

		# Not likely that we would ever get here, but try this:
		# Duplicate self and use as a counter to shift by int(1)
		counter = BitString(self._bits)
		zero = Zero(self._size)
		while counter > zero:
			# Try a single Python bit shift operation
			other = other << 1
			counter = counter.decrement()
		# Return whatever came out
		return other

	def __rrshift__(self, other):
		"Implement the >> right shift operation from the right side."

		# Not likely that we would ever get here, but try this:
		# Duplicate self and use as a counter to shift by int(1)
		counter = BitString(self._bits)
		zero = Zero(self._size)
		while counter > zero:
			# Try a single Python bit shift operation
			other = other >> 1
			counter = counter.decrement()
		# Return whatever came out
		return other

	def __rand__(self, other):
		"The right bitwise and of two bit strings, using the & operator."

		_bitstring_check(other, self._size)
		# If the check somehow doesn't fail, just reverse the operands
		return (self & other)

	def __rxor__(self, other):
		"The right bitwise xor of two bit strings, using the ^ operator."

		_bitstring_check(other, self._size)
		# If the check somehow doesn't fail, just reverse the operands
		return (self ^ other)

	def __ror__(self, other):
		"The right bitwise or of two bit strings, using the | operator."

		_bitstring_check(other, self._size)
		# If the check somehow doesn't fail, just reverse the operands
		return (self | other)

	# Augmented assignment bitwise operator methods

	def __ilshift__(self, other):
		"Implements augmented assignment with the <<= operator."
		
		# To avoid code duplication, just call the regular method
		return (self << other)

	def __irshift__(self, other):
		"Implements augmented assignment with the >>= operator."
		
		# To avoid code duplication, just call the regular method
		return (self >> other)

	def __iand__(self, other):
		"Implements augmented assignment with the &= operator."
		
		# To avoid code duplication, just call the regular method
		return (self & other)

	def __ixor__(self, other):
		"Implements augmented assignment with the ^= operator."
		
		# To avoid code duplication, just call the regular method
		return (self ^ other)

	def __ior__(self, other):
		"Implements augmented assignment with the |= operator."
		
		# To avoid code duplication, just call the regular method
		return (self | other)

	# Unary bitwise not method

	def __invert__(self):
		"Take the bitwise not of a bit string using the unary ~ operator."

		# Create a list to store the inverted bits
		not_bits = []
		# Invert each bit one at a time
		for i in xrange(self._size):
			not_bits.append(~(self._bits[i]))
		# Return the bits in a new bit string
		return BitString(tuple(not_bits))

	# Octal and hexadecimal methods

	def __oct__(self):
		"Print the value of the bit string in octal."

		# For octal, we want to take the bits in groups of 3
		group = 3
		# Make a table of the 8 octal digits and bit patterns
		digits = list("01234567")
		bits = Zero(group)
		table = {}
		for digit in digits:
			table[string_bits(bits)] = digit
			bits = bits.increment()
		# Take chunks of bits and gather the octal digits
		oct_list = []
		if self._size % group == 0:
			i = 0
		else:
			i = (self._size % group) - group
		while i < self._size:
			if i >= 0:
				chunk = BitString(self._bits[i:i+group], size=group)
			else:
				chunk = BitString(self._bits[0:i+group], size=group)
			oct_list.append(table[string_bits(chunk)])
			i += group
		# Add the prefix zero and return the string
		return '0' + "".join(oct_list).lstrip('0')

	def __hex__(self):
		"Print the value of the bit string in hexadecimal."

		# For hexadecimal, we want to take the bits in groups of 4
		group = 4
		# Make a table of the 16 hexadecimal digits and bit patterns
		digits = list("0123456789abcdef")
		bits = Zero(group)
		table = {}
		for digit in digits:
			table[string_bits(bits)] = digit
			bits = bits.increment()
		# Take chunks of bits and gather the hexadecimal digits
		hex_list = []
		if self._size % group == 0:
			i = 0
		else:
			i = (self._size % group) - group
		while i < self._size:
			if i >= 0:
				chunk = BitString(self._bits[i:i+group], size=group)
			else:
				chunk = BitString(self._bits[0:i+group], size=group)
			hex_list.append(table[string_bits(chunk)])
			i += group
		# Add the prefix 0x and return the string, checking for zero value
		hex_result = "0x" + "".join(hex_list).lstrip('0')
		return (hex_result if hex_result[-1] != 'x' else hex_result + '0')

	# Increment and decrement methods

	def increment(self):
		"Increase the binary value stored in a bit string by 1."

		# Copy the bit string's digits to a temporary list 
		new_bits = [b for b in self._bits]
		# Start at the smallest digit and work upwards
		for i in xrange(self._size - 1, -1, -1):
			# When adding 1, 0 becomes 1 and 1 becomes 0
			new_bits[i] = ~self._bits[i]
			# A result of 1 means there was no carry, so finish here
			if new_bits[i] == bit.One:
				break
		# Return the incremented value, do not increment in-place
		return BitString(tuple(new_bits))

	def decrement(self):
		"Decrease the binary value stored in a bit string by 1."

		# Copy the bit string's digits to a temporary list 
		new_bits = [b for b in self._bits]
		# Start at the smallest digit and work upwards
		for i in xrange(self._size - 1, -1, -1):
			# When subtracting 1, 0 becomes 1 and 1 becomes 0
			new_bits[i] = ~self._bits[i]
			# A result of 0 means there was no borrow, so finish here
			if new_bits[i] == bit.Zero:
				break
		# Return the decremented value, do not decrement in-place
		return BitString(tuple(new_bits))

# Bit string checking function

def _bitstring_check(obj, size=None):
	"Raise an error if obj is not a bit string or has the wrong size."

	if not isinstance(obj, BitString):
		raise TypeError("bit string operand required for bit string operation")
	# Check the size only if the size parameter is actually passed
	if size is not None and obj._size != size:
		raise ValueError("bit string operation with different bit string sizes")

# Simple bits printing function

def string_bits(bitstring):
	"Return a string containing zeros and ones for every bit in a bit string."

	_bitstring_check(bitstring)
	# Just return the string of each bit all stuck together
	return "".join([str(b) for b in bitstring._bits])

# Shortcut one-byte constructor

def Byte(value=None):
	"Construct a bit string of 8 bits with an optional value initializer."

	return BitString(binary=value, size=BYTE)

# Shortcut zero-value bit string constructor

def Zero(bits=None):
	"Construct a bit string with value 0 and optional number of bits."

	# Default the size to one byte if no size is given
	if bits is None:
		bits = BYTE
	return BitString(binary="0", size=bits)

# Bit string truncation and expansion functions

def truncate(bstr, new_size):
	"Return a given bit string with its data truncated to a given size."

	_bitstring_check(bstr)
	# Take the lowest bits and return a new bit string with desired size
	return BitString(bstr._bits[-new_size:], min(new_size, bstr._size))

def expand(bstr, new_size):
	"Return a given bit string with its size expanded to a given size."

	_bitstring_check(bstr)
	# Take the bits and return a new bit string with the larger size
	return BitString(bstr._bits, max(new_size, bstr._size))

# ASCII character functions

def to_char(byte):
	"Accept a bit string and return its corresponding ASCII character."

	# The bit string SHOULD be 8 bits, but doesn't NEED to be
	_bitstring_check(byte)
	# Decrement the byte to zero while incrementing a Python int
	zero = Zero(byte._size)
	value = 0
	while byte > zero:
		byte = byte.decrement()
		value += 1
	# Translate the Python int to a character with the chr function
	return chr(value)

def char_value(char):
	"Accept a character and return a bit string byte with its ASCII value."

	# Translate the character to a Python int with the ord function
	value = ord(char)
	# Decrement the Python int while incrementing a bit string from zero
	byte = Byte("0")
	while value > 0:
		value -= 1
		byte = byte.increment()
	# Return the now properly-set bit string
	return byte

# Code for testing the bit string class

if __name__ == "__main__":

	# Print message for the user
	print "Testing bit string class..."

	# Create function for generating random binary strings
	from random import randrange
	randstr = lambda d : "".join([str(randrange(2)) for i in xrange(d)])

	# Python int binary converter
	inb = lambda x : bin(x)[2:].lstrip('0')

	# A few controlling parameters for the trials
	trials = 10**4
	max_digits = 25

	# Test the constructor
	print "  Testing constructor"
	for t in xrange(trials):
		r1 = 1 + randrange(max_digits)
		r2 = 1 + randrange(max_digits)
		br = min(r1, r2)
		sr = max(r1, r2)
		s = randstr(br)
		b1 = BitString(size=r1)
		b2 = BitString(size=r2)
		assert len(string_bits(b1)) == r1
		assert len(string_bits(b2)) == r2
		assert b1._size == r1
		assert b2._size == r2
		b3 = BitString(s)
		b4 = BitString(s, br)
		b5 = BitString(s, sr)
		assert string_bits(b3) == string_bits(b4)
		assert len(string_bits(b3)) == br
		assert len(string_bits(b4)) == br
		assert b3._size == br
		assert b4._size == br
		assert string_bits(b5)[-br:] == string_bits(b3)
		assert string_bits(b5)[-br:] == string_bits(b4)
		assert string_bits(b5)[:-br] == '0' * (sr - br)
		assert len(string_bits(b5)) == sr
		assert b5._size == sr
		b6 = BitString(b1)
		b7 = BitString(b1._bits)
		b8 = BitString(b1, r1)
		b9 = BitString(b1._bits, r1)
		assert len(string_bits(b6)) == r1
		assert string_bits(b6) == string_bits(b1)
		assert string_bits(b6) == string_bits(b7)
		assert string_bits(b6) == string_bits(b8)
		assert string_bits(b6) == string_bits(b9)
		assert b6._size == r1
		assert b7._size == r1
		assert b8._size == r1
		assert b9._size == r1

	# Test the string bits function
	print "  Testing string bits function"
	for t in xrange(trials):
		s = randstr(max_digits)
		b = BitString(s)
		assert string_bits(b) == s

	# Test the representation methods
	print "  Testing representations"
	for t in xrange(trials):
		r = 1 + randrange(max_digits)
		s = randstr(r)
		b1 = BitString(s)
		b2 = BitString(s, r)
		rep = "BitString(\"%s\", %d)" % (s, r)
		assert b1 == b2
		assert repr(b1) == rep
		assert repr(b2) == rep
		assert str(b1) == str(b2)
		c1 = [len(a) for a in str(b1).split()]
		assert c1[0] == 1
		assert c1[-1] == 1
		assert c1[1] <= 4
		assert all([c == 4 for c in c1[2:-1]])

	# Test the comparison methods
	print "  Testing comparisons"
	for t in xrange(trials):
		r = 1 + randrange(max_digits)
		b1 = BitString(size=r)
		b2 = BitString(size=r)
		x1 = int(string_bits(b1), 2)
		x2 = int(string_bits(b2), 2)
		assert (b1 < b2) == (x1 < x2)
		assert (b1 <= b2) == (x1 <= x2)
		assert (b1 == b2) == (x1 == x2)
		assert (b1 != b2) == (x1 != x2)
		assert (b1 > b2) == (x1 > x2)
		assert (b1 >= b2) == (x1 >= x2)

	# Test the boolean converter
	print "  Testing bool"
	for t in xrange(trials):
		r = 1 + randrange(max_digits)
		b = BitString(size=r)
		x = int(string_bits(b), 2)
		assert bool(b) == bool(x)
		z = Zero(r)
		assert bool(z) == False

	# Test the bitwise operators
	print "  Testing bitwise operators"
	for t in xrange(trials):
		r1 = 1 + randrange(max_digits)
		r2 = 1 + randrange(max_digits/4)
		b1 = BitString(size=r1)
		b2 = BitString(size=r2)
		b3 = BitString(size=r1)
		x1 = int(string_bits(b1), 2)
		x2 = int(string_bits(b2), 2)
		x3 = int(string_bits(b3), 2)
		assert string_bits(b1 << b2).lstrip('0') == inb((x1 << x2) % 2**r1)
		assert string_bits(b1 >> b2).lstrip('0') == inb((x1 >> x2) % 2**r1)
		assert string_bits(b1 & b3).lstrip('0') == inb(x1 & x3)
		assert string_bits(b1 ^ b3).lstrip('0') == inb(x1 ^ x3)
		assert string_bits(b1 | b3).lstrip('0') == inb(x1 | x3)

	# Test the reflected bit shift operations
	print "  Testing reflected bit shifts"
	for t in xrange(trials):
		s1 = randstr(max_digits)
		s2 = randstr(max_digits/4)
		b2 = BitString(s2)
		x1 = int(s1, 2)
		x2 = int(s2, 2)
		assert (x1 << b2) == (x1 << x2)
		assert (x1 >> b2) == (x1 >> x2)

	# Test the unary bitwise not
	print "  Testing bitwise not"
	for t in xrange(trials):
		s = randstr(max_digits)
		b1 = BitString(s)
		b2 = ~b1
		assert b2 != b1
		assert (~b2) == b1
		not_bits = "".join([('0' if b == '1' else '1') for b in s])
		assert string_bits(b2) == not_bits

	# Test the oct and hex functions
	for t in xrange(trials):
		s = randstr(max_digits)
		b = BitString(s)
		x = int(s, 2)
		assert oct(b) == oct(x)
		assert hex(b) == hex(x)

	# Test the increment and decrement operators
	print "  Testing increment and decrement"
	for t in xrange(trials):
		s = randstr(max_digits)
		b = BitString(s)
		x = int(s, 2)
		bp = b.increment()
		bm = b.decrement()
		xp = (x + 1) % 2**max_digits
		xm = (x - 1) % 2**max_digits
		assert string_bits(bp).lstrip('0') == inb(xp)
		assert string_bits(bm).lstrip('0') == inb(xm)

	# Test the bit string checking function
	print "  Testing bit string checker"
	for o in [True, 1, 1.0, 1.0+1.0j, tuple(), {}, [], bit.Bit()]:
		error = False
		try:
			_bitstring_check(o)
		except TypeError:
			error = True
		assert error
	for t in xrange(trials):
		r1 = 1 + randrange(max_digits)
		r2 = 1 + randrange(max_digits)
		s1 = randstr(r1)
		b1 = BitString(s1)
		error = False
		try:
			_bitstring_check(b1, r2)
		except ValueError:
			error = True
		assert error == (r1 != r2)

	# Test the Byte and Zero constructors
	print "  Testing byte and zero constructors"
	for t in xrange(trials):
		r1 = randrange(2**BYTE)
		s1 = inb(r1)
		b1 = Byte(s1)
		s2 = string_bits(b1)
		assert len(s2) == BYTE
		assert int(s2, 2) == r1
		r2 = 1 + randrange(max_digits)
		b2 = Zero(r2)
		s3 = string_bits(b2)
		assert len(s3) == r2
		assert s3 == '0' * r2

	# Test the truncate and expand functions
	print "  Testing truncate and expand"
	for t in xrange(trials):
		r1 = 1 + randrange(max_digits)
		r2 = 1 + randrange(max_digits)
		r3 = 1 + randrange(max_digits)
		s1 = randstr(r1)
		b = BitString(s1)
		s2 = string_bits(truncate(b, r2))
		s3 = string_bits(expand(b, r3))
		assert len(s2) == min(r1, r2)
		assert len(s3) == max(r1, r3)
		assert s2 == s1[-len(s2):]
		assert s1 == s3[-len(s1):]
		assert s3[:-len(s1)] == '0' * (len(s3) - len(s1))

	# Test the ASCII character code functions
	print "  Testing ASCII functions"
	for x in xrange(2**BYTE):
		c = chr(x)
		s = inb(x)
		b = Byte(s)
		bc = to_char(b)
		bx = char_value(bc)
		assert bc == c
		assert bx == b

	# Print closing message
	print "All tests passed!"

