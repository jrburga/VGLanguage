# Used as an abstraction for multiple effects.
# Need to add that effects also apply to groups, not just instances.
def Chained(*effects):
	def effect(scene, condition):
		for effect in effects:
			effect(scene, condition)
	return effect

# need to do a check such that if the condition returns empty, it returns all
def IncrementResource((class_name, resource, value)):
	def effect(scene, condition):
		for instance in condition.instances[class_name]:
			for instance_resource in instance.resources:
				if instance_resource.name == resource:
					instance_resource.value += value
	return effect

def SetResource((class_name, resource, value)):
	def effect(scene, condition):
		for instance in condition.instances[class_name]:
			for resource in instance.resources:
				if resource.name == resource:
					resource.value = value
	return effect

def Kill((class_name, )):
	def effect(scene, condition):
		print condition.instances
		for instance in condition.instances[class_name]:
			print class_name, instance
			instance.kill()
	return effect

def Nothing(empty):
	def effect(scene, condition):
		pass
	return effect