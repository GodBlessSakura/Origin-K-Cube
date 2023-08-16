MATCH (user:User{userId: $userId})
WITH DISTINCT user
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})
WHERE EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace))
WITH DISTINCT workspace
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value