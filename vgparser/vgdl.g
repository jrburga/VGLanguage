//LveelDescription
level: header level_body
level_body: "Instances" class_instances+
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
vgdlclasses: class_hierarchy+
class_hierarchy: vgdlclass ["{" vgdlclasses "}"]
vgdlclass: name [":" props]
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
mapping: key_inputs [":" active_flag] ">" actions
actions: action ["," action]
key_inputs: name ["&" name]
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
// ****************

conditions: condition ["&" condition]
effects: effect ["," effect]
condition: neg? function
effect: function
function: name params
neg: "~"
params: "(" (param ["," param])? ")"
param: value | cmp

props: prop+
prop: key "=" value

value: number
	 | bool
     | name
     | vector

cmp: "="  -> eq
   | "<"  -> lt
   | ">"  -> gt
   | "!=" -> ne
   | ">=" -> le
   | "<=" -> ge

active_flag: "active" | "inactive"
name: UCAMEL -> string
key: USCORE -> string
number: SIGNED_NUMBER
vector: "(" number ("," number)* ")"
bool: "True"  -> true
	| "False" -> false

UCAMEL: /([A-Z]([a-zA-Z0-9])*)/
USCORE: /([a-z]([a-z_])*)/


COMMENT: "#"+ /./* NEWLINE

%import common.SIGNED_NUMBER
%import common.NEWLINE
%import common.WS

%ignore WS
%ignore COMMENT
%ignore NEWLINE