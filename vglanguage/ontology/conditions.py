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
			for name in instance.names:
				if name not in self._instances or name in rest:
					rest.add(name)
					self._instances[name].add(instance)
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
		self.classes = [class_name1, class_name2]
		self.colliding = False

		self.event_triggers = self.collision_triggers()

	def collision_triggers(self):
		# create event handler to raise collision flags
		def test(event):
			check = [False, False]
			check_r = [False, False]
			if self.classes[0] in event.game_objects[0].names:
				if self.classes[1]  in event.game_objects[1].names:
					return (True, (self.classes[0], self.classes[1]))

			if self.classes[0] in event.game_objects[1].names:
				if self.classes[1] in event.game_objects[0].names:
					return (True, (self.classes[1], self.classes[0]))

			return (False, None)


		def collision(scene, event):
			result, classes = test(event)
			if result:
				print 'collision', self.classes
				self.colliding = True
				self._instances[classes[0]].add(event.game_objects[0])
				self._instances[classes[1]].add(event.game_objects[1])
		def separation(scene, event):
			result, classes = test(event)
			if result:
				print 'separation', self.classes
				self.colliding = False
				self._instances[classes[0]].remove(event.game_objects[0])
				self._instances[classes[1]].remove(event.game_objects[1])

		return [('collision', collision), ('separation', separation)]

	def test(self):
		return self.colliding

if __name__ == '__main__':
	simple_scene = Scene()
	simple_scene.room._game_objects.add(Instance(Class('five')))
	# print simple_scene.room.game_objects
	collision_condition = Collision(('one', 'two'))
	another_collision_condition = Collision(('three', 'four'))
	comp = Composition(InstanceCondition())
	simple_scene.add_condition_handler(comp, lambda scene, condition: True)