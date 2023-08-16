MATCH
    (operator:User{userId: $operatorId})-[:USER_OWN]->(workspace:Workspace{deltaGraphId: $deltaGraphId}),
    (instructor:User{userId: $userId}),
    (instructor)-[assignment:USER_COAUTHOR]->(workspace)
DELETE assignment