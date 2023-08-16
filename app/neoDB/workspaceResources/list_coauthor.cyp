
MATCH (user:User), (workspace:Workspace{deltaGraphId: $deltaGraphId})
WHERE EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true})) OR EXISTS((user)-[:USER_COAUTHOR]->(workspace))
RETURN user, EXISTS((user)-[:USER_COAUTHOR]->(workspace)) as isCoauthoring