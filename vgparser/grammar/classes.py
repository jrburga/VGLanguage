class VGDLClass(object):
	def __init__(self, name, props={}):
		self.name = name
		self.props = {}
		self.props.update(props)
		self.children = []
		self.parent = None