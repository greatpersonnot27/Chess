class Vector2:
	"""
		This is a class for a two dimensional vector

		Attributes:

			data (tuple): tupe of x and y of the Vector
	"""
	def __init__(self, data):
		"""
		Constructs a Vector2 from a given tuple

		Parameters
		----------

		    data (tuple):

		        tuple of two integers
		"""
		if len(data) != 2:
			raise RuntimeError("Vector2 takes only iterable of length 2")
		self.data = tuple(data)
	
	def __add__(self, value):
		"""
		Overloads the add operator for two Vector2 - s

			Parameters:

				value (Vector2): Vector to be added

			Returns:

				(Vector2): Sum of two Vector2 - s

		"""
		if isinstance(value, Vector2):
			if len(value) != len(self.data):
				raise RuntimeError("unssuported operation on Vector")
			else:
				return Vector2([sum(i) for i in zip(value, self.data)])

		elif isinstance(value, int):
			return Vector2(tuple(i + value for i in self.data))

		else:
			raise RuntimeError("unssuported operation on Vector")
	
	def __truediv__(self, value):
		"""
		Overloads the division operator for two Vector2 - s

			Parameters:

				value (Vector2): Vector2 to be divided by

			Returns:

				(Vector2): Current vector divided by the Value

		"""
		return Vector2([i / value for i in self.data])
	
	def __floordiv__(self, value):
		"""
		Overloads the floor division operator for two Vector2 - s

			Parameters:

				value (Vector2): Vector2 to be divided by

			Returns:

				(Vector2): Current vector divided by the Value

		"""
		return Vector2([i // value for i in self.data])
	
	def __eq__(self, value):
		"""
		Overloads the equal to operator for two Vector2 - s

			Parameters:

				value (Vector2): Vector2 to be compared

			Returns:

				(bool): True if two vectors are the same, else false

		"""
		if len(self.data) != len(value):
			return False
		return tuple(value) == self.data
	
	def __getitem__(self, key):
		"""
		Overloads the bracket operator for the Vector2

			Parameters:

				key (integer): index of the Vector2 member

			Returns:

				(integer): value of the member at index key

		"""
		return self.data[key]
	
	def __setitem__(self, key, data):
		"""
		Overloads the set item operator for the Vector2

			Parameters:

				key (integer): index of the Vector2 member

				data (integer): value to be set for the given key
		"""
		self.data[key] =  data
	
	def __getitem__(self, key):
		return self.data[key]

	def __ne__(self, value):
		return not self.__eq__(value)
	
	def __sub__(self, value):
		"""
		Overloads the substitution operator for two Vector2 - s

			Parameters:

				value (Vector2): Vector to be subtracted

			Returns:

				(Vector2): subtraction of two Vector2 - s

		"""
		invert = tuple(i * -1  for i in value)
		return self.__add__(Vector2(invert))
	
	def __contains__(self, value):
		"""
		Overloads the contain operator

			Parameters:

				value (integer): value to be checked

			Returns:

				(bool): True if value is contained inside the Vector2, else false

		"""
		return value in self.data
	
	def __len__(self):
		"""
		Overloads the length operator

			Returns:

				(integer): length of the Vector2

		"""
		return len(self.data)
	
	def __abs__(self):
		"""
		Overloads the absolute value operator for a Vector2

			Returns:

				(Vector2): each member replace with its absolute value

		"""
		return Vector2([abs(i) for i in self.data])
	
	def __iter__(self):
		for i in self.data:
			yield i
	
	def __repr__(self):
		return self.data.__str__()
	
	@property
	def x(self):
		return self.data[0]
	
	@property
	def y(self):
		return self.data[1]
