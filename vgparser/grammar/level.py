
class Level(object):
	def __init__(self, header, body):
		assert 'instances' not in header
		self.__dict__.update(header)
		self.instances = body[:]

	def toJSON(self):
		pass

	# def __repr__(self):
	# 	return self.__dict__

	def __str__(self):
		return "%r" % self.__dict__
		

class Instance(object):
	def __init__(self, vgdlclass, position, orientation):
		self.class_name = vgdlclass
		self.position = position
		self.orientation = orientation
