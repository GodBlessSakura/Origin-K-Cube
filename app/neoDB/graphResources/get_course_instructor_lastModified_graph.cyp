MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MATCH (user:User{userId: $userId})-[:USER_TEACH]->(course)
MATCH (workspace:Workspace)<-[:USER_OWN]-(user)
WHERE split(workspace.deltaGraphId,'.')[0] = toString(id(course))
WITH collect(workspace) as workspaces, max(workspace.lastModified) as lastModified, course, user
WITH [w IN workspaces WHERE w.lastModified = lastModified][0] as workspace
RETURN workspace