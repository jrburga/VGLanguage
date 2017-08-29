from vgengine.systems import physics
from vgengine.systems import resources

#Actions for the action sets
# An action has attributes, though.

def Move((direction, speed)):
	print 'move with speed', speed
	def apply_direction(go):
		go.body.velocity = physics.Vec2d(direction)*speed
	return apply_direction

if __name__ == '__main__':
	print BasicMotion()