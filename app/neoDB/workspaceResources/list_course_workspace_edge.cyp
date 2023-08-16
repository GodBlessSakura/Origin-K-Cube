MATCH
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId}),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE
    split(workspace.deltaGraphId,'.')[0] = toString(id(course))
WITH DISTINCT workspace
MATCH
    (workspace)-[edges:WORK_ON]->()
RETURN DISTINCT edges
