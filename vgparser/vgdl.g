//LveelDescription
level: header instances
instances: "Instances" class_instances+
class_instances: name "{" instance_vecs "}"
instance_vecs: instance_vec+ 
instance_vec: vector

// GameDescription
// ****************
game: header game_body
header: name [":" props]
game_body: (classes
	  | groups
	  | actionsets
	  | terminationrules
	  | rules)+

// Classes
// ****************
classes: "Classes" vgdlclasses
vgdlclasses: vgdlclass+
vgdlclass: class_desc ["{" vgdlclasses "}"]
class_desc: name [":" props]
// ****************

// Groups
// ****************
groups: "Groups" group+
group: name ":" props
// ****************

// ActionSets
// ****************
actionsets: "ActionSets" actionset+
actionset: name "{" mappings "}"
mappings: mapping+
mapping: key_inputs ">" actions
actions: action ["," action]
key_inputs: key_input ["&" key_input]
key_input: name
action: function
// ****************

// TerminationRules
// ****************
terminationrules: "TerminationRules" terminationrule+
terminationrule: conditions [">" effects]
// ****************

// Rules
// ****************
rules: "Rules" rule+
rule: conditions ">" effects
conditions: condition ["&" condition]
effects: effect ["," effect]
condition: neg? function
effect: function

// ****************

props: prop+
prop: key "=" value

function: name params
params: "(" (param ("," param)*)? ")"
param: value | cmp
neg: "~"

vector: "(" number ("," number)* ")"

value: number
     | bool
     | name
     | vector
     | function

cmp: "="  -> eq
   | "<"  -> lt
   | ">"  -> gt
   | "!=" -> ne
   | ">=" -> le
   | "<=" -> ge

bool: "True"  -> true
  | "False" -> false

name: UCAMEL -> string
key: USCORE -> string
number: SIGNED_NUMBER

UCAMEL: /([A-Z]([a-zA-Z0-9])*)/
USCORE: /([a-z]([a-z_])*)/


COMMENT: "#"+ /./* NEWLINE

%import common.SIGNED_NUMBER
%import common.NEWLINE
%import common.WS

%ignore WS
%ignore COMMENT
%ignore NEWLINE