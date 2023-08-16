MATCH (h)-[r:META_RELATE]->(t)
RETURN DISTINCT h.name as h_name, r.name as r_name, t.name as t_name