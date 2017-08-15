from vgengine.game import *



class BasicRoom(Room):
	'''
	Should probably have some kind of edge detection involved.

	Also, should include information about object classes to make
	querying easier.
	'''

class BasicScene(Scene):
	'''
	A basic scene with one room.
	'''
	def __init__(self, size, fps):
		Scene.__init__(self, graphics.Graphics2D(size), physics.Physics2D(1./fps), resources.Resources())

	def add_instance(self, game_object):
		self.room.add(game_object)

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
		self.fps = fps
		Game.__init__(self, scene)


if __name__ == '__main__':
	scene = BasicScene((400, 400), 60)
