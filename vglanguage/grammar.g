// LevelDescription
// ****************
level: level_header level_desc
level_header: "Level" [":" assignments]
level_desc: class_instances+
class_instances: string "{" instances "}"
instances: instance+
instance: vector [":" assignments]

// GameDescription
// ***************
game: game_header game_desc
game_header: "Game" "<" (function | string) [":" assignments ":"]
game_desc: (class_set | groups_set | rules_set | termination_set | action_set)*

// ActionSets
// ***************
action_set: "ActionSets" type_sets
type_sets: type_set+
type_set: type_name "{" actions "}"
type_name: string
actions: action+
action: inputs ">" action_effects
action_effects: action_effect ("," action_effect)*
action_effect: string "(" [value ("," value)*] ")"
inputs: default_inputs | inactive_inputs
inactive_inputs: default_inputs ":" "inactive"
default_inputs: string ("&" string)*

// TerminationRules
// ***************
// Basically Rules, but with implicit effect
termination_set: "TerminationRules" termination_rules
termination_rules: termination_rule+
termination_rule: conditions [">" effects]


// Rules
// ***************
rules_set: "Rules" rules
rules: rule+
rule: conditions ">" effects
effects: effect ("," effect)*
effect: string "(" [value ("," value)*] ")"
conditions: condition ("&" condition)*
condition: function | negfunction

// GroupTypes
// ***************
// Pretty much equivalent to Classes
groups_set: "GroupTypes" classes

// Classes
// ***************
class_set: "Classes" classes
classes: class_desc+
class_desc: description ["{" classes "}"] 
description: classname [":" assignments ":"]
classname: string | compound_name
assignments: assignment+
assignment: string "=" (value | component)
component: string "(" [value ("," value)*] ")"

function: string "(" [value ("," value)*] ")"
negfunction: "~" function
compound_name: string ">" string 

value: string   
	| vector
     | number
     | "inf"  -> infinity
     | "True" -> true
     | "False"-> false
     | "*"    -> all
     | "="    -> eq
     | "!="   -> ne
     | "<="   -> le
     | ">="   -> ge
     | ">"    -> gt
     | "<"    -> lt
vector: "(" number ("," number)* ")"
string: CNAME 
number: SIGNED_NUMBER


COMMENT: "#"+ /./* NEWLINE

%import common.CNAME
%import common.WS
%import common.SIGNED_NUMBER
%import common.NEWLINE
%ignore WS
%ignore COMMENT
%ignore NEWLINE