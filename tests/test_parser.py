import unittest
from vgparser import parser

# print parser.Tree2PyVGDL

grammar = open('vgparser/vgdl.g').read()

class LevelTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='level',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_level(self):
		test_string = """
		Level1 : size=(100, 100)

		Instances

			Dog {
				(0, 0, 0)
				(1, 2, 3)
			}
			Cat {
				(4, 5, 0)
			}
		"""
		level = self.parser.parse(test_string)
		# print level

class LevelBodyTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='instances',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_body(self):
		test_string = '''
		Instances
		Dog {
			(0, 0, 0)
			(1, 2, 3)
		}
		Cat {
			(4, 5, 6)
		}
		'''
		body = self.parser.parse(test_string)
		# print body

class GameTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='game',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())
	def test_sample(self):
		test_string = '''
		TestGame
			Classes
				Dog
			Rules
				Condition() > Effect()
			Groups
				Animal : color=BLUE
			ActionSets
				UpDown {
					UP   > Move(0, 1)
					DOWN > Move(0, -1)
				}
			TerminationRules
				Condition()
		'''
		game = self.parser.parse(test_string)
		self.assertEqual(game.name, 'TestGame')
		print game


class ActionSets(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='actionset',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_actionsets(self):
		test_string = '''
		Basic {
			LEFT > Move()
		}
		'''
		actionset = self.parser.parse(test_string)
		# print actionsets[0].mappings[0]

	def test_multi_inputs(self):
		test_string = '''
		Basic {
			LEFT & RIGHT > Move()
		}
		'''
		actionset = self.parser.parse(test_string)
		# print actionsets[0].mappings[0]


class TerminationRulesTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='terminationrule',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())
	def test_termrules_simple(self):
		test_string = '''
		AllDead()
		'''
		termrule = self.parser.parse(test_string)
		self.assertEquals(len(termrule.conditions), 1)


class RuleTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='rule',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_rules_simple(self):
		test_string = '''Condition(Dog) > Effect(Dog)'''
		rule = self.parser.parse(test_string)
		self.assertEqual(len(rule.conditions), 1)
		self.assertEqual(len(rule.effects), 1)

	def test_rules_simple(self):
		test_string = '''Condition(Dog) > Effect(Dog), 
		Effect(Cat)'''
		rule = self.parser.parse(test_string)
		self.assertEqual(len(rule.conditions), 1)
		self.assertEqual(len(rule.effects), 2)
		

	def test_rule_empty_condition(self):
		test_string = '''Condition() > Effect(Dog)'''
		rule = self.parser.parse(test_string)
		self.assertEqual(rule.conditions[0].sign, "pos")


	def test_rule_neg_condition(self):
		test_string = '''~Condition() > Effect(Dog, Cat)'''
		rule = self.parser.parse(test_string)
		self.assertEqual(rule.conditions[0].sign, "neg")



class GroupsTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='groups',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_group_simple(self):
		test_string = '''
		Groups
			GroupA : strength = 100
		'''
		groups = self.parser.parse(test_string)['groups']
		self.assertEqual(len(groups), 1)
		group = groups[0]
		self.assertEqual(group.name, 'GroupA')

class ClassesTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='vgdlclasses', 
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_class_simple(self):
		test_string = '''
		Dog
		'''
		classes = self.parser.parse(test_string)
		self.assertEqual(len(classes), 1)
		child = classes[0]
		self.assertEqual(child.name, 'Dog')

	def test_class_two(self):
		test_string = '''
		Dog
		Cat
		'''
		classes = self.parser.parse(test_string)
		self.assertEqual(len(classes), 2)
	

	def test_class_props(self):
		test_string = '''
		Dog : strength=100
		'''
		classes = self.parser.parse(test_string)
		self.assertEqual(len(classes), 1)
		child = classes[0]
		self.assertEqual(child.props['strength'], 100)

	def test_class_syntax(self):
		test_string = '''
		Dog : strength=100
		Cat : strength=50
		'''
		classes = self.parser.parse(test_string)
		self.assertEqual(len(classes), 2)
		cat = [child for child in classes if child.name == 'Cat'][0]
		self.assertEqual(cat.props['strength'], 50)

	def test_class_hierarchy(self):
		test_string = '''
		Animal {
			Dog 
			Cat
		}
		'''
		classes = self.parser.parse(test_string)
		self.assertEqual(len(classes), 1)
		animal = classes[0]
		self.assertEqual(len(animal.children), 2)

	def test_class_hierarchy_with_props(self):
		test_string = '''
		Animal : strength = 100 {
			Dog 
			Cat
		}
		'''
		classes = self.parser.parse(test_string)
		animal = classes[0]
		self.assertEqual(animal.props['strength'], 100)
		# cat = [child for child in classes if child.name == 'Cat'][0]
		# self.assertEqual(cat.p

	def test_class_hierarchy_with_child_props(self):
		test_string = '''
		Animal : strength = 50 {
			Dog : strength = 100
		}	
		'''
		classes = self.parser.parse(test_string)
		animal = classes[0]
		dog = animal.children[0]
		self.assertEqual(dog.props['strength'], 100)
		self.assertEqual(animal.props['strength'], 50)

	def test_class_inline_props(self):
		test_string = '''
		Animal : strength = 100 dexterity = 50
		'''
		classes = self.parser.parse(test_string)
		animal = classes[0]
		self.assertEqual(animal.props['strength'], 100)
		self.assertEqual(animal.props['dexterity'],  50)

	def test_class_multiline_props(self):
		test_string = '''
		Animal : strength = 100
		         dexterity = 50
		'''
		classes = self.parser.parse(test_string)
		animal = classes[0]
		self.assertEqual(animal.props['strength'], 100)
		self.assertEqual(animal.props['dexterity'],  50)