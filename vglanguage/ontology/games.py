from vgengine.game import *

def quit(scene, event):
	scene.quit()

class BasicRoom(Room):
	'''
	Should probably have some kind of edge detection involved.

	Also, should include information about object classes to make
	querying easier.
	'''
	pass
	

class BasicScene(Scene):
	'''
	A basic scene with one room.
	'''
	def __init__(self, size, fps):
		Scene.__init__(self, graphics.Graphics2D(size), physics.Physics2D(1./fps), resources.Resources())
		self.graphics.camera.size = size
		self.fps = fps
		self._condition_handlers = defaultdict(lambda: [])

		self.add_event_handler('quit', quit)

	def add_condition_handler(self, condition, callback):
		condition.scene = self
		for event_trigger in condition.event_triggers:
			self.add_event_handler(event_trigger[0], event_trigger[1])
		self._condition_handlers[condition].append(callback)

	def _handle_conditions(self):
		for condition in self._condition_handlers:
			if condition.check(self):
				for callback in self._condition_handlers[condition]:
					callback(self, condition)

	def step(self):
		# In order for conditions to work, need to handle events first
		self._handle_events()
		self._handle_conditions()
		self._update_systems()

	def add_instance(self, game_object):
		self.room.add(game_object)

	def get_instances(self):
		return self.room.game_objects

class BasicGame(Game):
	'''
	Default graphics, physics, and resources used.
	Only set size and fps.

	A basic game only has one room, scene, and camera.

	The camera won't move, and the the edges of the camera
	(the edges of the screen) are used as the bounds to the 
	world.
	'''
	def __init__(self, scene):
		Game.__init__(self, scene)
		self.fps = scene.fps

	def run(self):
		super(BasicGame, self).run(self.fps)


if __name__ == '__main__':
	scene = BasicScene((400, 400), 60)
