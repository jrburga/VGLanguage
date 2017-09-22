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

		# self.basic_room = BasicRoom()
		self.basic_scene = BasicScene((300, 300), 60)

		self.basic_scene.add_instance(Instance(salmon))
		self.basic_scene.add_instance(Instance(goose))
		self.basic_scene.add_instance(Instance(duck))

	def test_case(self):
		# print self.basic_room.game_objects
		self.assertEqual(True, True)
		self.assertTrue(True)
		self.assertFalse(False)

	def test_new_test_name(self):
		self.assertTrue(True)