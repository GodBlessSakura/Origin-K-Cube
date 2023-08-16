MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId}),
    (user:User{userId: $userId})
RETURN EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace)) as is_coauthor_or_owner