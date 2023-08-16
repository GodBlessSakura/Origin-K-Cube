MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId}),(user:User{userId: $userId})
WHERE EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace))
WITH DISTINCT workspace
MATCH (h:GraphConcept{name: $h_name})
MATCH (t:GraphConcept{name: $t_name})
MATCH (h) -[r:DELTA_GRAPH_RELATIONSHIP{name: $r_name, deltaGraphId : workspace.deltaGraphId}]-> (t)
WITH h.name as h_name, r.name as r_name, t.name as t_name, r, workspace
DELETE r
SET workspace.lastModified = datetime.transaction()
RETURN h_name, r_name, t_name;