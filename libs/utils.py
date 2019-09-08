class Vector2:
	def __init__(self, data):
		if len(data) != 2:
			raise RuntimeError("Vector2 takes only iterable of length 2")
		self.data = tuple(data)
	
	def __add__(self, value):
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
		return Vector2([i / value for i in self.data])
	
	def __floordiv__(self, value):
		return Vector2([i // value for i in self.data])
	
	def __eq__(self, value):
		if len(self.data) != len(value):
			return False
		return tuple(value) == self.data
	
	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, data):
		self.data[key] =  data
	
	def __getitem__(self, key):
		return self.data[key]

	def __ne__(self, value):
		return not self.__eq__(value)
	
	def __sub__(self, value):
		invert = tuple(i * -1  for i in value)
		return self.__add__(Vector2(invert))
	
	def __contains__(self, value):
		return value in self.data
	
	def __len__(self):
		return len(self.data)
	
	def __abs__(self):
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
