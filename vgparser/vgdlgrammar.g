// GameDescription
// ****************
game_description: game_header game_body
game_header: "Game"
game_body: ( classes
		   | groups
		   | rules
		   | termination_rules
		   | actions_sets)*

// Classes
// ****************
classes: "Classes" vgdlclass+
vgdlclass: NAME -> name
class_descs: class_desc+
class_desc: description
description: class_name [":" assignments]



// Rules
// ****************
rules_set: "Rules" rules
rules: rule+
rule: condition+ ">" effect+
condition: 
effect: 

NAME: /([A-Z][a-z])/

COMMENT: "#"+ /./* NEWLINE

%import common.NEWLINE
%import common.WS
%import common.UCASE_LETTER
%import common.LCASE_LETTER

%ignore WS
%ignore COMMENT
%ignore NEWLINE