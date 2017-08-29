from vgengine.systems import graphics, physics, resources
print 'components being used'

def DYNAMIC(mass):
	return physics.Body2D(mass)

def STATIC(mass):
	return physics.StaticBody2D()

def KINEMATIC(mass):
	return physics.KinematicBody2D()

def RECT(size, color):
	rect = graphics.RectSprite2D(size, color=color)
	shape = physics.BoxShape2D(size)
	return set([rect, shape])

def CIRCLE(radius, color):
	circle = graphics.CircleSprite2D(int(radius[0]), color=color)
	shape = physics.CircleShape2D(radius[0])
	return set([circle, shape])

def RESOURCE(name, *args):
	return resources.Resource(name, *args)

class Keyboard(resources.Controller):
	def update(self):
		self.inputs = []
		if graphics._pygame.key.get_pressed()[graphics.K_UP]:
			self.inputs.append('UP')

		if graphics._pygame.key.get_pressed()[graphics.K_LEFT]:
			self.inputs.append('LEFT')

		if graphics._pygame.key.get_pressed()[graphics.K_RIGHT]:
			self.inputs.append('RIGHT')

		if graphics._pygame.key.get_pressed()[graphics.K_DOWN]:
			self.inputs.append('DOWN')

		if graphics._pygame.key.get_presesd()[graphics.K_SPACE]:
			self.inputs.append('A')

		if not self.inputs:
			self.inputs.append('NONE')


def Move((direction, speed)):
	print 'move with speed', speed
	def apply_direction(go):
		go.body.velocity = physics.Vec2d(direction)*speed
	return apply_direction
