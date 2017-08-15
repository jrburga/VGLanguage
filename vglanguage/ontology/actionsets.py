from vgengine.systems import physics

#Actions for the action sets
# An action has attributes, though.

def move(direction, speed):
	def apply_direction(go):
		go.body.velocity = physics.Vec2d(direction)*speed
	return apply_direction
