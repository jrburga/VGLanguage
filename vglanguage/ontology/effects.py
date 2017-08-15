def Chained(*effects):
	def effect(scene, condition):
		for effect in effects:
			effect(scene, condition)
	return effect

# need to do a check such that if the condition returns empty, it returns all
def IncrementResource(class_name, resource, value):
	def effect(scene, condition):
		for instance in condition.instances[class_name]:
			for resource in instance.resources:
				if resource.name == resource:
					resource.value += value
	return effect

def SetResource(class_name, resource, value):
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
			instance.kill()
	return effect