MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (owner)-[:USER_OWN]->(workspace:Workspace{deltaGraphId: $deltaGraphId})-[:WORK_ON]->(subject)
WITH DISTINCT subject
MATCH (ancestor)<-[:PATCH|FORK*]-(subject)
WITH collect(ancestor.deltaGraphId) + [subject.deltaGraphId] AS deltaGraphIds
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP]->(t:GraphConcept)
where r.deltaGraphId IN deltaGraphIds
WITH h.name AS h_name, r.name AS r_name, t.name AS t_name, max(r.creationDate) AS r_creationDate, deltaGraphIds
MATCH (h:GraphConcept{name: h_name})-[r:DELTA_GRAPH_RELATIONSHIP{name: r_name, creationDate: r_creationDate}]->(t:GraphConcept{name: t_name})
WHERE r.deltaGraphId IN deltaGraphIds
RETURN h.name, r.name, t.name, r.value