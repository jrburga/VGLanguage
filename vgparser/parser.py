from lark import Lark, Transformer
from collections import defaultdict

from grammar import *

# grammar = open('vgdlgrammar.g').read()
class Tree2PyVGDL(Transformer):

	def header(self, header):
		name = header[0]
		props = header[1] if len(header) > 1 else {}
		header = {'name': header[0]}
		header.update(props)
		return header

	# Level
	#####################
	def level(self, level):
		return Level(*level)

	def instances(self, instances):
		all_instances = []
		for instance_list in instances:
			all_instances += instance_list
		return all_instances

	def class_instances(self, (name, vecs)):
		instances = []
		for pos, ori in vecs:
			instances.append(Instance(name, pos, ori))
		
		return instances

	def instance_vecs(self, vecs):
		return vecs


	def instance_vec(self, (vec, )):
		return vec[:2], vec[2]

	#####################
	#

	# Game
	#####################
	def game(self, game):
		return Game(*game)

	def game_body(self, args):
		body = {}
		for arg in args:
			body.update(arg)
		return body
	######################
	#

	# Classes 
	###################
	def classes(self, (classes, )):
		return {'classes': classes}

	def vgdlclasses(self, vgdlclasses):
		return vgdlclasses

	def vgdlclass(self, vgdlclass):
		children = vgdlclass[1] if len(vgdlclass) > 1 else []
		vgdlclass = vgdlclass[0]
		vgdlclass['children'] = children
		return VGDLClass(**vgdlclass)

	def class_desc(self, class_desc):
		desc = {}
		desc['name'] = class_desc[0]
		desc['props'] = class_desc[1] if len(class_desc) > 1 else {}
		return desc
	####################
	# 

	# Groups 
	####################
	def groups(self, groups):
		return {'groups': groups}
		
	def group(self, vgdlgroup):
		name = vgdlgroup[0]
		props = vgdlgroup[1:]
		if props: props = props[0]
		return Group(name, props)
	####################
	#

	# Rules 
	###################
	def rules(self, rules):
		return {'rules': rules}

	def rule(self, rule):
		return Rule(*rule)

	def effects(self, effects):
		return effects

	def conditions(self, conditions):	
		return conditions

	def condition(self, condition):
		sign = condition[0] if len(condition) > 1 else "pos"
		condition = condition[-1]
		condition['sign'] = sign
		return Condition(**condition)

	def effect(self, (effect, )):
		return Effect(**effect)
	###################
	#

	# Termination Rules 
	###################
	def terminationrules(self, terminationrules):
		return {'termination_rules': terminationrules}

	def terminationrule(self, terminationrule):
		return TerminationRule(*terminationrule)
		
	###################
	#

	# Action Sets
	###################
	def actionsets(self, actionsets):
		return {'action_sets': actionsets}

	def actionset(self, actionset):
		name, mappings = actionset
		return ActionSet(name, mappings)

	def mappings(self, mappings):
		return mappings

	def mapping(self, (key_inputs, actions)):
		return Mapping(key_inputs, actions)

	def actions(self, actions):
		return actions

	def action(self, (action, )):
		return Action(**action)

	def key_inputs(self, key_inputs):
		return key_inputs

	def key_input(self, (name, )):
		return KeyInput(name)

	###################
	#

	def function(self, (name, params)):
		return {'name': name, 'params': params}

	def params(self, params=[]):
		return params

	def param(self, (param, )):
		return param

	def props(self, props):
		return {k: v for d in props for k, v in d.items()}


	def prop(self, (key, value)):
		return {key: value}

	def value(self, (value, )):
		return value

	def vector(self, values):
		return tuple(values)

	def string(self, (string, )):
		return str(string)

	def number(self, (number, )):
		return float(number)

	neg = lambda self, _: "neg" # lambda func: not func()

	true = lambda self, : True
	false = lambda self, _: False

	eq = lambda self, _: "eq" # lambda x, y: x == y
	lt = lambda self, _: "lt" # lambda x, y: x < y
	gt = lambda self, _: "gt" # lambda x, y: x > y
	ne = lambda self, _: "ne" # lambda x, y: x != y
	le = lambda self, _: "le" # lambda x, y: x >= y
	ge = lambda self, _: "ge" # lambda x, y: x <= y


# with open('vgdlgrammar.g') as g:
# 	game_parser = Lark(g.read(), start='game', parser='lalr', transformer=Tree2PyVGDL())

# with open('vgdlgrammar.g') as g:
# 	level_parser = Lark(g.read(), start='level', parser='lalr', transformer=Tree2PyVGDL())

# def parse_game(game_string):
# 	return game_parser.parse(game_string)

# def parse_level(level_string):
# 	return level_parser.parse(level_string)