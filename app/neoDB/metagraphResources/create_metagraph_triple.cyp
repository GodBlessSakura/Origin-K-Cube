MATCH (h:MetaConcept{name: $h_name}),(t:MetaConcept{name: $t_name})
WITH DISTINCT h, t
MERGE (h)-[r:META_RELATE{name: $r_name}]->(t)
RETURN h.name as h_name, r.name as r_name, t.name as t_name