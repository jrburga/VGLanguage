import unittest
from vgparser import parser

# print parser.Tree2PyVGDL

grammar = open('vgparser/vgdlgrammar.g').read()

class GameTest(unittest.TestCase):
	def setUp(self):
		pass
	
	def test_sample(self):
		self.assertTrue(True)

class ActionSets(unittest.TestCase):
	def setUp(self):
		pass

	def test_actionsets(self):
		

class TerminationRulesTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='terminationrules',
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())
	def test_termrules_simple(self):
		test_string = '''
		TerminationRules
			AllDead()
		'''
		termrules = self.parser.parse(test_string)
		self.assertEquals(len(termrules), 1)
		self.assertEquals(len(termrules[0].conditions), 1)


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
		

	def test_rule_empty_condition(self):
		test_string = '''Condition() > Effect(Dog)'''
		rule = self.parser.parse(test_string)


	def test_rule_neg_condition(self):
		test_string = '''~Condition() > Effect(Dog)'''
		rule = self.parser.parse(test_string)



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
		groups = self.parser.parse(test_string)
		self.assertEqual(len(groups), 1)
		group = groups[0]
		self.assertEqual(group.name, 'GroupA')

class ClassesTest(unittest.TestCase):
	def setUp(self):
		self.parser = parser.Lark(grammar, 
								  start='classes', 
								  parser='lalr',
								  transformer=parser.Tree2PyVGDL())

	def test_class_simple(self):
		test_string = '''
		Classes
			Dog
		'''
		root_class = self.parser.parse(test_string)
		self.assertEqual(len(root_class.children), 1)
		child = root_class.children[0]
		self.assertEqual(child.name, 'Dog')

	def test_class_two(self):
		test_string = '''
		Classes
			Dog
			Cat
		'''
		root_class = self.parser.parse(test_string)
		self.assertEqual(len(root_class.children), 2)
	

	def test_class_props(self):
		test_string = '''
		Classes
			Dog : strength=100
		'''
		root_class = self.parser.parse(test_string)
		self.assertEqual(len(root_class.children), 1)
		child = root_class.children[0]
		self.assertEqual(child.props['strength'], 100)

	def test_class_syntax(self):
		test_string = '''
		Classes
			Dog : strength=100
			Cat : strength=50
		'''
		root_class = self.parser.parse(test_string)
		self.assertEqual(len(root_class.children), 2)
		cat = [child for child in root_class.children if child.name == 'Cat'][0]
		self.assertEqual(cat.props['strength'], 50)

	def test_class_hierarchy(self):
		test_string = '''
		Classes
			Animal {
				Dog 
				Cat
			}
		'''
		root_class = self.parser.parse(test_string)
		self.assertEqual(len(root_class.children), 1)
		animal = root_class.children[0]
		self.assertEqual(len(animal.children), 2)

	def test_class_hierarchy_with_props(self):
		test_string = '''
		Classes
			Animal : strength = 100 {
				Dog 
				Cat
			}
		'''
		root_class = self.parser.parse(test_string)
		animal = root_class.children[0]
		self.assertEqual(animal.props['strength'], 100)
		# cat = [child for child in root_class.children if child.name == 'Cat'][0]
		# self.assertEqual(cat.p

	def test_class_hierarchy_with_child_props(self):
		test_string = '''
		Classes
			Animal : strength = 50 {
				Dog : strength = 100
			}
		'''
		root_class = self.parser.parse(test_string)
		animal = root_class.children[0]
		dog = animal.children[0]
		self.assertEqual(dog.props['strength'], 100)
		self.assertEqual(animal.props['strength'], 50)

	def test_class_inline_props(self):
		test_string = '''
		Classes
			Animal : strength = 100 dexterity = 50
		'''
		root_class = self.parser.parse(test_string)
		animal = root_class.children[0]
		self.assertEqual(animal.props['strength'], 100)
		self.assertEqual(animal.props['dexterity'],  50)

	def test_class_multiline_props(self):
		test_string = '''
		Classes
			Animal : strength = 100
					 dexterity = 50
		'''
		root_class = self.parser.parse(test_string)
		animal = root_class.children[0]
		self.assertEqual(animal.props['strength'], 100)
		self.assertEqual(animal.props['dexterity'],  50)