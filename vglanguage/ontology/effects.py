# Used as an abstraction for the parser to generate the effects used by the game.
# Need to add that effects also apply to groups, not just instances.
def Chain(*effects):
	def effect(scene, condition):
		for fx in effects:
			fx(scene, condition)
	return effect

def EmptyEffect(apply_effect):
	def effect(scene, condition):
		apply_effect()
	return effect

def InstanceEffect(class_name, args, apply_effect):
	def effect(scene, condition):
		for instance in condition.instances[class_name]:
			if args:
				apply_effect(instance, args)
			else:
				apply_effect(instance)
	return effect

# the actual effects

def IncrementResource(instance, (resource, value)):
	instance.resources[resource].value += value

def SetResource(instance, (resource, value)):
	instance.resources[resource].value = value

def Kill(instance):
	print 'killing -- ', instance, instance.components
	instance.kill()
	# print instance.components

def Nothing():
	pass