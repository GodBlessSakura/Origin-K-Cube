MATCH (h:MetaConcept{name: $h_name})-[r:META_RELATE{name: $r_name}]->(t:MetaConcept{name: $t_name})
DELETE r
RETURN h.name as h_name, $r_name as r_name, t.name as t_name