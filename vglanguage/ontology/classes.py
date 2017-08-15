class Class(object):
	'''
	A simple container for classes and their properties
	'''
	def __init__(self, name):
		self.name = name
		self.props = {}
		self._parent = None
		self.children = []

	@property
	def parent(self):
		return self._parent

	@parent.setter
	def parent(self, new_parent):
		if self.parent:
			self.parent.children.remove(self)
		self._parent = new_parent
		new_parent.children.append(self)

	def get_prop(self, prop_name):
		if prop_name in self.props:
			return self.props[prop_name]
		elif self.parent:
			return self.parent.get_prop(prop_name)

class Root(Class):
	'''
	Class with a few default properties
	'''
	def __init__(self):
		Class.__init__(self, 'root')
		self.props = {
			'mass' : 5
		}