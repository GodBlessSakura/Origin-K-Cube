MATCH
    (user:User{userId: $userId}),
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner:User)
WHERE EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace))
WITH DISTINCT owner, workspace
MATCH
    (course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
RETURN workspace, course, EXISTS((course)<-[:BRANCH_DESCRIBE]-(workspace)) as isExposed, owner