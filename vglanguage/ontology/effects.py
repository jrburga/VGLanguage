# Used as an abstraction for the parser to generate the effects used by the game.
# Need to add that effects also apply to groups, not just instances.

from copy import deepcopy

def Combo(*actions):
	def action(go):
		for ax in actions:
			ax(go)
	return action

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
		instances = set()
		if class_name in condition.instances:
			for instance in condition.instances[class_name]:
				instances.add(instance)
		else:
			for instance in scene.room.game_objects:
				
				if class_name in instance.names:
					instances.add(instance)
					
		for instance in instances:
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