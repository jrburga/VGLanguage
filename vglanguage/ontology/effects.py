# Used as an abstraction for the parser to generate the effects used by the game.
# Need to add that effects also apply to groups, not just instances.
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
				apply_effect(scene, instance, *args)
			else:
				apply_effect(scene, instance)
	return effect

# the actual effects

def IncrementAttribute(scene, instance, attr, value):
	if hasattr(instance, attr):
		setattr(instance, attr, getattr(instance, attr) + value)
	elif attr in instance.resources:
		instance.resources[attr].value += value
	else:
		raise NameError('instance does not have attribute or resource')
	

def SetAttribute(scene, instance, attr, value):
	if hasattr(instance, attr):
		setattr(instance, attr, value)
	elif attr in instance.resources:
		instance.resources[resource].value = value

# Toggle Action? Need to be certain of activation/deactivation, though.
def ActivateAction(scene, instance, action_name):
	pass

def DeactiveAction(scene, instance, action_name):
	pass

# It's unclear to me what these function would actually do
# Do they just change their names?
# Do they also change all their properties to align with their new class/group?
def ChangeGroup(scene, instance, group_name):
	pass

def ChangeClass(scene, instance, class_name):
	pass

# 
# Could create problems with the physics? I know that objects
# that are directly on top of each other are resolved smoothly,
# but it could be weird.
def Clone(scene, instance):
	'''Makes a copy of the instance at the instance's location.'''
	pass

def Kill(scene, instance):
	# print 'killing -- ', instance, instance.components
	instance.kill()
	# print instance.components

def Create(scene, class_name, position, orientation):
	# Wait, actually, now that thing about not having access to the whole game object is kind of a problem
	pass

# Non deterministic events.
def Teleport(scene, instance, class_name2):
	'''Randomly moves instance to an instance of class_name2'''
	pass

def Spawn(scene, class_name1, class_name2):
	'''Randomly creates an instance of class_name1 at the location of class_name2'''
	pass
	
def Nothing(scene):
	pass