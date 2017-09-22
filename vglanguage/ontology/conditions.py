from collections import defaultdict
from objects import *

class Condition(object):
	def __init__(self):
		self.event_triggers = []

	def check(self, scene):
		return False

class InstanceCondition(Condition):
	def __init__(self):
		Condition.__init__(self)
		self._instances = defaultdict(lambda: set())

	@property
	def instances(self):
		return self._instances

# Some useful classes probably.
class Composition(InstanceCondition):
	def __init__(self, *conditions):
		# print 'composition'
		super(Composition, self).__init__()
		self.conditions = conditions
		for condition in conditions:
			self.event_triggers.extend(condition.event_triggers[:])

	@property
	def instances(self):
		self._instances = defaultdict(lambda: set())
		for condition in self.conditions:
			for class_name in condition.instances: #instances is a dict
				self._instances[class_name] = self._instances[class_name].union(condition.instances[class_name])
		return self._instances

	def check(self, scene):
		return reduce(lambda x, y: x and y, [con.check(scene) for con in self.conditions], True)

class Not(InstanceCondition):
	def __init__(self, condition):
		super(Not, self).__init__()
		self.condition = condition
		self.event_triggers = condition.event_triggers[:]

	@property
	def instances(self):
		'''Return the compliment sets?'''
		return self.condition.instances

	def check(self, scene):
		return not self.condition.check()

# The rest of the conditions
class Collision(InstanceCondition):
	def __init__(self, class_name1, class_name2):
		super(Collision, self).__init__()
		self.classes = [class_name1, class_name2]
		self.colliding = False

		self.event_triggers = self._collision_triggers()

	def _collision_triggers(self):
		# create event handler to raise collision flags
		def check(event):
			if self.classes[0] in event.game_objects[0].names:
				if self.classes[1]  in event.game_objects[1].names:
					return (True, (self.classes[0], self.classes[1]))

			if self.classes[0] in event.game_objects[1].names:
				if self.classes[1] in event.game_objects[0].names:
					return (True, (self.classes[1], self.classes[0]))

			return (False, None)


		def collision(scene, event):
			result, classes = check(event)
			if result:
				print 'collision', self.classes
				self.colliding = True
				self._instances[classes[0]].add(event.game_objects[0])
				self._instances[classes[1]].add(event.game_objects[1])

		def separation(scene, event):
			result, classes = check(event)
			if result:
				print 'separation', self.classes
				self.colliding = False
				if event.game_objects[0] in self._instances[classes[0]]:
					self._instances[classes[0]].remove(event.game_objects[0])
				if event.game_objects[1] in self._instances[classes[1]]:
					self._instances[classes[1]].remove(event.game_objects[1])

		return [('collision', collision), ('separation', separation)]

	def check(self, scene):
		for instance in scene.instances:
			for colliding_objects in instance.collision_set:
				
		return self.colliding

class InstanceCount(InstanceCondition):
	def __init__(self, class_name, value, operator):
		super(InstanceCount, self).__init__()
		self._op = operator
		self.value = value
		self.class_name = class_name
	def check(self, scene):
		self._instances[self.class_name] = set()
		for instance in scene.get_instances():
			if self.class_name in instance.names:
				self._instances[self.class_name].add(instance)
		if self._op(len(self._instances[self.class_name]), self.value):
			return True
		return False

# I just realized, this is going to be parsed in the language...
class CreationCondition(InstanceCondition):
	def __init__(self, class_name, event_name):
		super(CreationCondition, self).__init__()
		self.class_name = class_name
		self.event_triggers = self._creation_triggers(event_name)
		self.instance_set = set()
		self.creation_flag = False
		self.type = event_name

	def _creation_triggers(self, event_name):
		def trigger(scene, event):
			# print 'creation condition triggered', self.type, self.class_name
			if self.class_name in event.game_object.names:
				# print 'creation condition triggered', self.type
				self.instance_set.add(event.game_object)
				self.creation_flag = True

		return [(event_name, trigger)]

	def check(self, scene):
		if self.instance_set:
			self._instances[self.class_name] = self.instance_set
		self.instance_set = set()
		creation_flag = self.creation_flag
		self.creation_flag = False
		return creation_flag

class Killed(CreationCondition):
	def __init__(self, class_name):
		super(Killed, self).__init__(class_name[0], 'kill')


class Created(CreationCondition):
	def __init__(self, class_name):
		super(Created, self).__init__(class_name[0], 'create')


# if __name__ == '__main__':
# 	simple_scene = Scene()
# 	simple_scene.room._game_objects.add(Instance(Class('five')))
# 	# print simple_scene.room.game_objects
# 	collision_condition = Collision(('one', 'two'))
# 	another_collision_condition = Collision(('three', 'four'))
# 	comp = Composition(InstanceCondition())
# 	simple_scene.add_condition_handler(comp, lambda scene, condition: True)