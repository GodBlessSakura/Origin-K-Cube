MATCH 
    (user:User{userId: $userId}),
    (owner)-[:USER_OWN]->(workspace:Workspace{deltaGraphId: $deltaGraphId}),
    (workspace)-[:WORK_ON]->(subject)
WHERE EXISTS((user)-[:USER_COAUTHOR]->(workspace)) OR EXISTS((user)-[:USER_OWN]->(workspace))
WITH DISTINCT user, workspace, subject, owner
MATCH (course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH subject, user, course, owner
OPTIONAL MATCH (subject)-[:PATCH|FORK]->(predecessor)
MATCH (course)-[:COURSE_DESCRIBE]->(courseConcept)
RETURN subject, NOT EXISTS((subject)<-[:PATCH]-()) as isPatchLeaf, user.userId = owner.userId as isOwner, courseConcept.name as courseCode, EXISTS((course)<-[:BRANCH_DESCRIBE]-(subject)) as isExposed, EXISTS((owner)-[:USER_TEACH]->(course)) as isTeaching, predecessor.deltaGraphId as predecessor