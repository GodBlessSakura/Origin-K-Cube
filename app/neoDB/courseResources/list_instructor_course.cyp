MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept),(user{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canViewInternalCourse:true})
WITH distinct user, course, courseConcept
OPTIONAL MATCH
    (workspace:Workspace)<-[:USER_OWN]-(user)
WHERE split(workspace.deltaGraphId,'.')[0] = toString(id(course))
WITH collect(workspace) as workspaces, max(workspace.lastModified) as lastModified, user, course, courseConcept
WITH [w IN workspaces WHERE w.lastModified = lastModified] as workspaces, user, course, courseConcept
RETURN course, courseConcept, EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching, workspaces, EXISTS((course)<-[:BRANCH_DESCRIBE{userId: $userId}]-()) as hasExposedGraph