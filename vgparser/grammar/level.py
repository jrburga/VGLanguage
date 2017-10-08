
class Level(object):
	def __init__(self, header, instances):
		assert 'instances' not in header
		self.__dict__.update(header)
		self.instances = instances[:]

	def toJSON(self):
		json = self.__dict__
		json.instances = [i.toJSON() for i in self.instances]
		return json

	def __str__(self):
		return "%r" % self.__dict__
		

class Instance(object):
	def __init__(self, vgdlclass, position, orientation):
		self.class_name = vgdlclass
		self.position = position
		self.orientation = orientation

	def toJSON(self):
		return self.__dict__
