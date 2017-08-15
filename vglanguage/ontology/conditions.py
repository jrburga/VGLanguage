from vgengine.game import Condition, Event, Scene
from collections import defaultdict
from instances import Instance
from classes import Class

class InstanceCondition(Condition):
	def __init__(self):
		Condition.__init__(self)
		self._instances = defaultdict(lambda: set())
		self._scene = None

	@property
	def scene(self):
		return self._scene

	@scene.setter
	def scene(self, new_scene):
		self._scene = new_scene

	@property
	def instances(self):
		rest = set()
		for instance in self.scene.room.game_objects:
			if instance.name not in self._instances or instance.name in rest:
				rest.add(instance.name)
				self._instances[instance.name].add(instance)
		return self._instances

# Some useful classes probably.
class Composition(InstanceCondition):
	def __init__(self, *conditions):
		super(Composition, self).__init__()
		self.conditions = conditions
		for condition in conditions:
			self.event_triggers.extend(condition.event_triggers)

	@property
	def scene(self):
		return self._scene

	@scene.setter
	def scene(self, new_scene):
		self._scene = new_scene
		for condition in self.conditions:
			condition.scene = new_scene

	@property
	def instances(self):
		self._instances = defaultdict(lambda: set())
		for condition in self.conditions:
			for class_name in condition.instances:
				self._instances[class_name] = self._instances[class_name].union(condition.instances[class_name])
		return super(Composition, self).instances

	def test(self):
		for condition in self.conditions:
			condition.scene = self.scene
		return reduce(lambda x, y: x and y, [con.test() for con in self.conditions], True)

class Not(InstanceCondition):
	def __init__(self, condition):
		super(Not, self).__init__()
		self.condition = condition

	@property
	def scene(self):
		return self._scene

	@scene.setter
	def scene(self, new_scene):
		self._scene = new_scene
		self.condition.scene = new_scene

	@property
	def instances(self):
		return self.condition.instances

	def test(self):
		return not self.condition.test()

# The rest of the conditions
class Collision(InstanceCondition):
	def __init__(self, (class_name1, class_name2)):
		super(Collision, self).__init__()
		self.classes = set([class_name1, class_name2])
		self.colliding = False

		self.event_triggers = self.collision_triggers()

	def collision_triggers(self):
		# create event handler to raise collision flags
		test = lambda event: set([event.go1.name, event.go2.name]) == self.classes
		def collision(self, scene, event):
			print 'collision'
			if test(event):
				self.colliding = True
				self.instances[event.go1.name].append(event.go1)
				self.instances[event.go2.name].append(event.go2)
		def separation(self, scene, event):
			print 'separate'
			if test(event):
				self.colliding = False
				self.instances[event.go1.name].remove(event.go1)
				self.instances[event.go2.name].remove(event.go1)

		return [('collision', collision), ('separate', separation)]

	def test(self):
		print self, self.colliding
		return self.colliding

if __name__ == '__main__':
	simple_scene = Scene()
	simple_scene.room._game_objects.add(Instance(Class('five')))
	# print simple_scene.room.game_objects
	collision_condition = Collision(('one', 'two'))
	another_collision_condition = Collision(('three', 'four'))
	comp = Composition(InstanceCondition())
	simple_scene.add_condition_handler(comp, lambda scene, condition: True)