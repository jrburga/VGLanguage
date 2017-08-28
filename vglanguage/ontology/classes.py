class Class(object):
	'''
	A simple container for classes and their properties
	'''
	def __init__(self, name):
		self.name = name
		self._props = {}
		self._parent = None
		self.children = []

	@property
	def names(self):
		names = [self.name]
		if self.parent:
			names += self.parent.names
		return names

	@property
	def subclasses(self):
		subclasses = []
		for child in self.children:
			subclasses += [child] + child.subclasses
		return subclasses

	@property
	def leaves(self):
		leaves = []
		for child in self.children:
			if child.children:
				leaves += child.leaves
			else:
				leaves += [child]
		return leaves

	@property
	def parent(self):
		return self._parent

	@parent.setter
	def parent(self, new_parent):
		if self.parent:
			self.parent.children.remove(self)
		self._parent = new_parent
		self._parent.children.append(self)

	def get_prop(self, prop_name):
		if prop_name in self._props:
			return self._props[prop_name]
		elif self.parent:
			return self.parent.get_prop(prop_name)
		else:
			return None

	def create_components(self):
		return ()

class Root(Class):
	'''
	Class with a few default properties
	'''
	def __init__(self):
		Class.__init__(self, 'root')
		self._props = {
			'mass'   : 5,
			'gravity': None,
			'color'  : 'white'
		}

class RECT(object):
	def __init__(self, size):
		print 'creating rect'