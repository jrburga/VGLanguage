# What if I defined everything this way?
# The problem is, these could be drastically improved using the builtin callbacks/event loop
import random as _random

def Collision(scene, class_name1, class_name2):
	'''
	Stupidly iterate over the collisions in the scene again
	and return True if an instance of class_name1 is colliding with class_name2
	'''
	return 

def Rule(conditions, effects):
	
	return callback



def Adjacent(scene, class_name1, class_name2):
	'''
	Define what it means to be adjacent
	return true if instance of class_name1 is adjacent to class_name2
	'''
	return False

def Distance(scene, class_name1, class_name2, value, operator):
	'''
  	Stupidly calculate the distance between every object
  	return True if distance operator \in {<, <=, =, >=, >} 
  	value between instance of class_name1 and class_name2 is
  	'''  
  	return False

def AttributesCompare(scene, class_name1, class_name2, attr_name, op):
	'''
	Stupidly iterate over each object pair and and compare the given attribute.
	What happens if one (or both) of the objects don't have the attribute?
	'''
	return False

def AttributeValue(scene, class_name1, attr_name, value, op):
	'''
	Stupidly iterate over each object and compare the attribute to the value
	'''
	return False

def Killed(scene, class_name):
	'''
	Returns True if an instance of class_name died in the last step
	'''
	return False

def Created(scene, class_name):
	'''
	Returns True if an instance of class_name was created in the last step
	'''
	return False

def InstanceCount(scene, class_name, value, op):
	'''
	Returns True if the number of instances of class_name compare (via op)
	'''
	return False

def ClassCount(scene, class_name, value, op):
	'''
	Returns True if the number of classes of class_name compare (via op)
	'''
	return False

# Effects: These might be more reasonably defined as such


def Kill(scene, instance):
	instance.kill()

# def Create(scene, class_name, position, orientation):
# 	scene.create_instance(class_name, position, orientation) # ? is this how I want it ?

def SpawnAtLocation(scene, class_name1, position, orientation=0):
	scene.create_instance(class_name1, position, orientation)

def SpawnAtInstance(scene, class_name1, class_name2):
	instance = _random.choice(scene.get_instance(class_name2))
	scene.create_instance(class_name1, instance.position, instance.orientation)

def TeleportToLocation(scene, instance, position, orientation=0):
	instance.position = position
	instance.orientation = orientation

def TeleportToInstance(scene, instance, class_name):
	instance2 = _random.choice(scene.get_instance(class_name))
	instance.position = instance2.position
	instance.orientation = orientation

def Clone(scene, instance):
	# scene.create_instance(instance.name, instance.position, instance.orientation)
	scene.add(instance.clone())

def IncrementAttribute(scene, instance, attr_name, value):
	if hasattr(instance, attr_name):
		setattr(instance, attr_name, getattr(instance, attr_name) + value)
	elif attr_name in instance.resources:
		instance.resources[attr_name] += value

def SetAttribute(scene, instance, attr_name, value):
	if hasattr(instance, attr_name):
		setattr(instanec, attr_name, value)
	elif attr_name in instance.resources:
		instance.resources[attr_name] = value


def ChangeGroup(scene, instance, group_name):
	pass

def ChangeClass(scene, instance, class_name):
	pass

def ActivateAction(scene, instance, action_name):
	instance.actionset.deactivate_action(action_name)