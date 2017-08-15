from lark import Lark, Transformer
from collections import defaultdict

from ontology import *

import pprint

class Tree2Game(Transformer):

	def level(self, (header, level_desc)):
		return header, level_desc
	def level_header(self, assignments):
		return assignments
	def level_desc(self, class_instances):
		full = {}
		for class_instance in class_instances:
			full.update(class_instance)
		return full
	def class_instances(self, (name, instances)):
		return {name: instances}
	def instances(self, instances):
		return instances
	def instance(self, instance):
		if len(instance) < 2:
			instance.append({})
		return {'transform': instance[0], 
				'attributes': instance[1]}

	def game(self, (header, desc)):
		return header, desc
	def game_header(self, arguments):
		arguments[0]
		return arguments
	def game_desc(self, game_desc):
		all_descs = {}
		for desc in game_desc:
			all_descs.update(desc)
		return all_descs

	def action_set(self, (action_set, )):
		return {'action_set': action_set}
	def type_sets(self, type_sets):
		all_sets = {}
		for type_set in type_sets:
			all_sets.update(type_set)
		return all_sets
	def type_set(self, (type_name, actions)):
		return {type_name: actions}
	def type_name(self, (type_name, )):
		return type_name
	def actions(self, actions):
		return actions
	def action(self, (inputs, effects)):
		inputs['effects'] = effects
		return inputs
	def inputs(self, (inputs, )):
		return inputs
	def default_inputs(self, inputs):
		return {'inputs': inputs, 'active': True}
	def inactive_inputs(self, (inputs, )):
		inputs['active'] = False
		return inputs


	def termination_set(self, (termination_set, )):
		return {'termination_rules': termination_set}
	def termination_rules(self, termination_rules):
		return termination_rules
	def termination_rule(self, rule):
		return rule
	def rules_set(self, (rules_set, )):
		return {'rules': rules_set}

	def rules(self, rules):
		return rules
	def rule(self, rule):
		return rule
	def effects(self, effects):
		return effects

	def conditions(self, conditions):
		return conditions
	def condition(self, (condition, )):
		return condition

	def groups_set(self, (groups, )):
		return {'groups': groups}

	def class_set(self, (classes, )):
		root = Root()
		for _class in classes:
			_class.parent = root
		return {'classes': root}

	def classes(self, classes):
		return classes

	def class_desc(self, args):
		_class = args[0]
		if len(args) > 1:
			for child in args[1]:
				child.parent = _class
		return _class

	def description(self, args):
		if len(args) > 1:
			args[0].props = args[1]
		return args[0]


	def classname(self, (classname, )):
		# print classname
		return Class(str(classname))

	# def simple_name(self, (classname, )):
	# 	return str(classname)

	def compound_name(self, (first, second)):
		return str(first)

	def assignments(self, props):
		# print props
		all_props = {}
		for prop in props:
			all_props.update(prop)

		return all_props

	def assignment(self, (key, value)):
		return {key: value}

	def prop(self, (prop, )):
		return prop	

	def value(self, (value, )):
		return value

	def string (self, (string, )):
		return str(string)

	def number(self, (number, )):
		return float(number)

	def vector(self, vector):
		return tuple(vector)

	def function(self, args):
		return args

	def negfunction(self, (function, )):
		function.insert(0, '~')
		return function

	true  = lambda self, _: True
	false = lambda self, _: False



with open('grammar.g') as g:
	game_parser = Lark(g.read(), start='game', parser='lalr', transformer=Tree2Game())

with open('grammar.g') as g:
	level_parser = Lark(g.read(), start='level', parser='lalr', transformer=Tree2Game())
	

# 	def class(self, description):

if __name__ == '__main__':
	game_string = '''
Game < SideView : gravity=(0, -10)
#################################
#   Comments are pretty cool    #
#################################  
Classes  # This is a Comment
	ClassName :something=else bool=False function=function (1, 1) {
		ChildClass : more=args {
			SubChildClass
			multiClass
		}
	}
	SuperClass > Predefined : arguments=10 {
		SubClass 
	}
	SingleClass

Rules
	~condition(arg, arg) & condition(part) > effect(1), effect(3)
	another(arg) > effect(3)

GroupTypes
	GroupType1

TerminationRules
	condition(arg) & another(arg) > effect(arg)

ActionSets
	Basic {
		INPUT1 & INPUT4 : inactive > Action(arguments), Action(arguments)
		INPUT2 & INPUT5 > Action(arguments)
	}
	Another {
		INPUT3 > Action(arguments)
	}
	'''

	level_string = '''
Level
Player {
	(44, 201, 3.1) : health=100 color=BLUE
	(33, 10, 10)
}
Enemy {
	(20.1, 2, 0) : controller=Random
}
'''
	pp = pprint.PrettyPrinter(indent=4)
	game = game_parser.parse(game_string)
	level = level_parser.parse(level_string)

	print game[1]['classes']

	pp.pprint(game)
	pp.pprint(level)
	

