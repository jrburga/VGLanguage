# need to do a check such that if the condition returns empty, it returns all
def IncrementResource(class_name, resource, value):
	def effect(self, scene, condition):
		for instance in condition.instances[class_name]:
			for resource in instance.resources:
				if resource.name == resource:
					resource.value += value
	return effect

def SetResource(class_name, resource, value):
	def effect(self, scene, condition):
		for instance in condition.instances[class_name]:
			for resource in instance.resources:
				if resource.name == resource:
					resource.value = value
	return effect

def Kill(class_name):
	def effect(self, scene, condition):
		for instance in condition.instances[class_name]:
			instance.kill()
	return effect