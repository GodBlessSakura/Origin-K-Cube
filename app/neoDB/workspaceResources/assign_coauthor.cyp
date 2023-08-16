MATCH
    (operator:User{userId: $operatorId})-[:USER_OWN]->(workspace:Workspace{deltaGraphId: $deltaGraphId}),
    (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})
MERGE (instructor)-[:USER_COAUTHOR]->(workspace)