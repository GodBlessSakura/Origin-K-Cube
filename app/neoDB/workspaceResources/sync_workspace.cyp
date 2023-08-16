MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner)
WITH DISTINCT workspace
MATCH (workspace)-[old:WORK_ON]->(subject)<-[:PATCH*]-(leaf)
WHERE NOT EXISTS((leaf)<-[:PATCH]-())
DELETE old
MERGE (workspace)-[:WORK_ON]->(leaf)
RETURN workspace