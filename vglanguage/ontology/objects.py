from vgengine import game
from vgengine.systems import graphics, physics, resources
# from cbd import 
from collections import defaultdict
from components import *

class Class(object):
	'''
	A simple container for classes and their properties
	'''
	def __init__(self, name):
		self.name = name
		self._props = {}
		self._parent = None
		self.children = []
		self.instances = set()
		self.components = set()

	def find(self, name):
		if self.name == name: 
			return self
		else:
			for subclass in self.subclasses:
				if subclass.name == name:
					return subclass


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

	def set_prop(self, prop_name, value):
		self._props[prop_name] = value


	def create_instance(self):
		return Instance(self)

	def create_components(self):
		created_components = set()

		for prop in self._props:
			value = self._props[prop]
			if isinstance(value, list):
				if value[0] == RESOURCE:
					created_components.add(value[0](prop, *value[1]))
		
		body = eval(self.get_prop('bodytype'))
		created_components.add(body(self.get_prop('mass')))

		shape, size = self.get_prop('shape')
		created_components.update(shape(size, self.get_prop('color')))

		controller = self.get_prop('controller')
		if controller:
			created_components.add(eval(controller)())

		actionset = self.get_prop('actionset')
		actions = {}
		if actionset:
			for action in actionset:
				# print action['effects']
				actions.update({action['inputs'][0]: action['effects']})
			# print 'actions', actions
		created_components.add(resources.ActionSet(actions))
		return created_components


class Root(Class):
	'''
	Class with a few default properties
	'''
	def __init__(self):
		super(Root, self).__init__('root')
		self._props = {
			'mass'      : 5,
			'gravity'   : None,
			'color'     : 'white',
			'bodytype'  : 'DYNAMIC',
			'shape'     : [RECT, (10, 10)],
			'controller': None,
			'actionset' : None, 
			'velocity'  : (0, 0),
			'elasticity': 0.0,
			'friction'  : 0.5
		}


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
		self._class = _class
		super(Instance, self).__init__(
			*_class.create_components()
		)

		# print self.body.gravity

		# for shape in self.body.shapes:
		# 	print 'elasticity', shape.elasticity


		if _class.get_prop('gravity') != None:
			self.body.gravity = _class.get_prop('gravity')

		if _class.get_prop('velocity'):
			self.body.velocity = _class.get_prop('velocity')

		if _class.get_prop('elasticity'):
			# print _class.get_prop('elasticity')
			for shape in self.body.shapes:
				shape.elasticity = _class.get_prop('elasticity')

		if _class.get_prop('friction'):
			for shape in self.body.shapes:
				shape.friction = _class.get_prop('friction')
				
		# for shape in self.body.shapes:
		# 	print 'elasticity', shape.elasticity
		self.group = None
		

		self._class.instances.add(self)


	def kill(self):
		game.Event(self.system_trigger, 'kill', **{'game_object': self}).trigger()
		self._class.instances.remove(self)
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

	# Of course this was causing a bug....
	# @property
	# def controller(self):
	# 	controllers = self.get_comoponents(resources.Controller)
	# 	if controllers:
	# 		return controllers[0]
	# 	return None

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
 	def orientation(self):
 		'''
		Angle in radians
 		'''
 		if self.body:
 			return self.body.angle

 	@orientation.setter
 	def orientation(self, new_orientation):
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

 	@property
 	def collision_set(self):
 		collision_set = set()
 		for shape in self.body.shapes:
 			collision_set.update(set([c.parent for c in shape.collision_set]))
 		return collision_set
		
	def __str__(self):
		return '<'+self.name+' instance '+str(id(self))+'>' 

	def __repr__(self):
		return self.__str__()