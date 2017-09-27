level: " "

// GameDescription
// ****************
game: header body
header: "Game"
body: (classes
	  | groups)

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
function: name "(" (param ["," param])? ")"
neg: "~"
param: name | value

props: prop+
prop: key "=" value

active_flag: "active" | "inactive"
name: UCAMEL -> string
key: LCAMEL -> string

value: NUMBER  -> number
     | "True"  -> true
     | "False" -> false

UCAMEL: /([A-Z]([a-z]|[A-Z])*)/
LCAMEL: /([a-z]([a-z]|[A-Z])*)/


COMMENT: "#"+ /./* NEWLINE

%import common.NUMBER
%import common.NEWLINE
%import common.WS

%ignore WS
%ignore COMMENT
%ignore NEWLINE