from vgengine.game import Condition, Event, Scene
from collections import defaultdict
from instances import Instance
from classes import Class

# create event handler to raise collision flags
def trigger_collision(col_con):
	check = lambda event: set([event.go1.name, event.go2.name]) == col_con.classes
	def collision(self, scene, event):
		if check(event):
			col_con.colliding = True
			col_con.instances[event.go1.name].append(event.go1)
			col_con.instances[event.go2.name].append(event.go2)
	def separation(self, scene, event):
		if check(event):
			col_con.colliding = False
			col_con.instances[event.go1.name].remove(event.go1)
			col_con.instances[event.go2.name].remove(event.go1)

	return collision, separation

class InstanceCondition(Condition):
	def __init__(self, scene):
		Condition.__init__(self, scene)
		self._instances = defaultdict(lambda: set())

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
	def __init__(self, scene, *conditions):
		super(Composition, self).__init__(scene)
		self.conditions = conditions

	@property
	def instances(self):
		self._instances = defaultdict(lambda: set())
		for condition in self.conditions:
			for class_name in condition.instances:
				self._instances[class_name] = self._instances[class_name].union(condition.instances[class_name])
		return super(Composition, self).instances

	def check(self):
		return reduce(lambda x, y: x and y, [con.check() for con in self.conditions], True)

class Not(InstanceCondition):
	def __init__(self, scene, condition):
		super(Not, self).__init__(scene)
		self.condition = condition

	@property
	def instances(self):
		return self.condition.instances

	def check(self):
		return not self.condition.check(self.scene)

# The rest of the conditions
class Collision(InstanceCondition):
	def __init__(self, scene, (class_name1, class_name2)):
		super(Collision, self).__init__(scene)
		self.classes = set([class_name1, class_name2])
		self.colliding = False

		scene.add_event_handler('collision', trigger_collision(self))
	def check(self):
		return self.colliding

if __name__ == '__main__':
	simple_scene = Scene()
	simple_scene.room._game_objects.add(Instance(Class('five')))
	# print simple_scene.room.game_objects
	collision_condition = Collision(simple_scene, ('one', 'two'))
	another_collision_condition = Collision(simple_scene, ('three', 'four'))
	comp = Composition(simple_scene, InstanceCondition(simple_scene))