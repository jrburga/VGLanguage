from vgengine.systems import graphics, resources

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