MATCH 
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId}),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE split(workspace.deltaGraphId,'.')[0] = toString(id(course))
RETURN DISTINCT workspace AS nodes, EXISTS((user)-[:USER_OWN]->(:Branch)<-[:WORK_ON]-(workspace)) AS canPatch
