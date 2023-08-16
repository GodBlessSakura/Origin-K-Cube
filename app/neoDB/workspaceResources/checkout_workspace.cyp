MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner)
WITH DISTINCT workspace
MATCH
    (workspace)-[old:WORK_ON]->(subject),
    (newSubject{deltaGraphId: $checkout})
DELETE old
MERGE (workspace)-[:WORK_ON]->(newSubject)
RETURN workspace