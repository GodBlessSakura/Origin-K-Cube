MATCH 
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId}),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE split(workspace.deltaGraphId,'.')[0] = toString(id(course))
WITH workspace, max(workspace.lastModified) as lastModified
WHERE workspace.lastModified = lastModified
RETURN DISTINCT workspace