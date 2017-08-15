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
		game.GameObject.__init__(self)
		self.group = None
		self._class = _class

	@property
	def name(self):
		return self._class.name

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
 		return self.get_components(resources.Resource)
		