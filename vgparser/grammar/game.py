KEYWORDS = ['classes', 'groups', 'rules', 'termination_rules', 'action_sets']

class FuncObj(object):
	def __init__(self, name, params):
		self.name = name
		self.params = params

	def toJSON(self):
		return {'name': self.name, 'params': self.params}	

class Game(object):
	def __init__(self, header, body):
		assert set(KEYWORDS).isdisjoint(set(header.keys()))
		self.__dict__.update(header)
		self.__dict__.update(body)

	def toJSON(self):
		json = self.__dict__
		for key_word in KEYWORDS:
			if key_word not in json.keys():
				json[key_word] = []
			else:
				json[key_word] = [v_type.toJSON() for v_type in json[key_word]]
		return json

# Group and VGDLClass
class Group(object):
	def __init__(self, name, props={}):
		self.name = name
		self.props = {}
		self.props.update(props)

	def toJSON(self):
		return {'name': self.name, 'props': self.props}

class VGDLClass(Group):
	def __init__(self, name, props={}, children=[]):
		super(VGDLClass, self).__init__(name, props)
		self.children = children[:]

	def toJSON(self):
		json = {}
		json.update(super(VGDLClass, self).toJSON())
		json['children'] = [child.toJSON() for child in self.children]
		return json

	def __str__(self):
		return 'VGDLClass: %s%r' % (self.name, self.props)

	def __repr__(self):
		return self.__str__()

#Action Sets
class ActionSet(object):
	def __init__(self, name, mappings):
		self.name = name
		self.mappings = mappings[:]

	def toJSON(self):
		return {'name': self.name, 
				'mappings': [mapping.toJSON() for mapping in self.mappings]}

class Mapping(object):
	def __init__(self, key_inputs, actions):
		# print key_inputs, actio
		self.key_inputs = key_inputs
		self.actions = actions

	def toJSON(self):
		return {
				'inputs' : [ki.toJSON() for ki in self.key_inputs],
				'actions': [act.toJSON() for act in self.actions] 
			   }

class Action(FuncObj):
	def __init__(self, name, params):
		super(Action, self).__init__(name, params)

class KeyInput(object):
	def __init__(self, name):
		self.name = name

	def toJSON(self):
		return self.name

#Rules
class Rule(object):
	'''A condition > effect container'''
	def __init__(self, conditions, effects):
		self.conditions = conditions[:]
		self.effects = effects[:]

	def toJSON(self):
		return {"conditions": [condition.toJSON() for condition in self.conditions],
				"effects": [effect.toJSON() for effect in self.effects]}

class TerminationRule(Rule):
	'''A special kind of rule that ends the game (as well as optional effects)'''
	def __init__(self, conditions, effects=[]):
		super(TerminationRule, self).__init__(conditions, effects)

class Condition(FuncObj):
	def __init__(self, name, params, sign="pos"):
		super(Condition, self).__init__(name, params)
		self.sign = sign

class Effect(FuncObj):
	def __init__(self, name, params):
		super(Effect, self).__init__(name, params)