MATCH (user:User{userId: $userId})
WITH DISTINCT user
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})-[:WORK_ON]->(subject)
WHERE EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace))
WITH DISTINCT subject
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value