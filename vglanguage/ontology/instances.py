from vgengine import game
from vgengine.systems import graphics, physics, resources
from collections import defaultdict
'''
In general, the Collider and the Shape are the same.

Internal attributes:
	Controller, ActionSet (ActionSet Properties), mass (inertia), grouping
External:
	Position, Speed, Direction, shape, color
'''
class Instance(game.GameObject):
	'''
	What a game instance in a VGDL world will look like (probably)
	'''
	def __init__(self, _class):
		'''
		grabs all the necessary properties from the class
		and its parents and applies them to the instance
		'''
		super(Instance, self).__init__(
			# _class.create_components()
			physics.Body2D(5),
			physics.BoxShape2D((10, 10)), 
			graphics.RectSprite2D((10, 10), color=_class.get_prop('color'))
		)
		# print self.body.gravity

		if _class.get_prop('gravity') != None:
			self.body.gravity = _class.get_prop('gravity')
		self.group = None
		self._class = _class

	def kill(self):
		print self.room
		if self.room:
			self.room.remove(self)

	@property
	def name(self):
		return self._class.name

	@property
	def names(self):
		return self._class.names

	@property
	def parent(self):
		return self._class.parent

	@property
	def controller(self):
		controllers = self.get_comoponents(resources.Controller)
		if controllers:
			return controllers[0]
		return None

	@property
	def actionset(self):
		actionsets = self.get_components(resources.ActionSet)
		if actionsets:
			return actionsets[0]

	@property
	def gravity(self):
		if self.body:
			return self.body.gravity
 
 	@property
 	def position(self):
 		if self.body:
 			return self.body.position

 	@position.setter
 	def position(self, new_position):
 		if self.body:
 			self.body.position = new_position

 	@property
 	def velocity(self):
 		if self.body:
 			return self.body.velocity

 	@velocity.setter
 	def velocity(self, new_velocity):
 		if self.body:
 			self.body.velocity = new_velocity

 	@property
 	def speed(self):
 		if self.body:
 			return self.body.velocity.length

 	@property
 	def direction(self):
 		if self.body and self.body.velocity:
 			return self.body.velocity.get_angle()

 	@property
 	def rotation(self):
 		'''
		Angle in radians
 		'''
 		if self.body:
 			return self.body.angle

 	@rotation.setter
 	def rotation(self, new_orientation):
 		'''
		Angle in radians
 		'''
 		if self.body:
 			self.body.angle = new_orientation

 	@property
 	def appearance(self):
 		return None

 	@property
 	def resources(self):
 		r = {}
 		for resource in self.get_components(resources.Resource):
 			r[resource.name] = resource
 		return r
		
	def __str__(self):
		return '<'+self.name+' instance '+str(id(self))+'>' 

	def __repr__(self):
		return self.__str__()