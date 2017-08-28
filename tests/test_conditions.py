import unittest

from vglanguage.ontology import *

class ConditionsTest(unittest.TestCase):
	def setUp(self):
		root = Root()

		bird = Class('Bird')
		duck = Class('Duck')
		goose = Class('Goose')

		fish = Class('Fish')
		salmon = Class('Salmon')

		fish.parent = root
		salmon.parent = fish

		bird.parent = root
		duck.parent = bird
		goose.parent = bird

		self.basic_room = BasicRoom()

		self.basic_room.add(Instance(salmon), Instance(goose), Instance(duck))

	def test_case(self):
		print self.basic_room.game_objects
		self.assertEqual(True, True)
		self.assertTrue(True)
		self.assertFalse(False)