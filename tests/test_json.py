import unittest
from vgparser.grammar import *
import json
from vgparser import parser

import pprint

grammar = open('vgparser/vgdl.g').read()
# print parser.Tree2PyVGDL
# class GameTest(unittest.TestCase):
# 	pass

class Test2Json(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='game',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())
	def test_func_obj(self):
		func_obj = FuncObj('Condition', [1, 2, 3])
		d = func_obj.toJSON()	
		self.assertEqual(d['name'], 'Condition')
		self.assertEqual(d['params'], [1, 2, 3])


	def test_vgdl_class(self):
		vgdl_class = VGDLClass('Dog', {'health': 100})
		d = vgdl_class.toJSON()
		self.assertEqual(d['name'], 'Dog')
		self.assertEqual(d['props']['health'], 100)

	def test_vgdl_class_hierarchy(self):
		dog = VGDLClass('Dog')
		cat = VGDLClass('Cat')
		animal = VGDLClass('Animal', children=[dog, cat])
		d = animal.toJSON()
		self.assertEqual(set([child['name'] for child in d['children']]), 
						 set(['Dog', 'Cat']))

	def test_group(self):
		group = Group('BlueThings')
		d = group.toJSON()
		self.assertEqual(d['name'], 'BlueThings')

	def test_game(self):
		test_string = '''
		TestGame : game_type=SideView gravity=1.0
			Classes
				Animal : strength=100{
					Dog : stamina=10
					Cat : stamina=20
				}
			Rules
				Collision(Dog, Cat) > Kill(Cat)
				Distance(Dog, Cat, 10, <) > ChangeController(Cat, Flee),
											ChangeController(Dog, Chase)

			Groups
				BlueThings : color=BLUE

			ActionSets
				Basic {
					UP    > Move(0, 1)
					DOWN  > Move(0, -1)
					LEFT  > Move(-1, 0)
					RIGHT > Move(1, 0)
				}
			TerminationRules
				InstanceCount(Cat, 0, =)
		'''
		game = self.parser.parse(test_string)
		d = game.toJSON()
		dumps = json.dumps(d)
		pprint.pprint(d)

		j = file('example_desc.json', 'w')
		j.write(dumps)


		self.assertEqual(d['name'], 'TestGame')
		self.assertEqual(d['game_type'], 'SideView')