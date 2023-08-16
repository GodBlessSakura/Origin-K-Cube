MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MATCH (user:User{userId: $userId})-[:USER_TEACH]->(course)
WITH course, user
CALL{
    WITH course, user
    MATCH (course)<-[:BRANCH_DESCRIBE{userId: user.userId}]-(graph:Branch)
    RETURN graph
UNION
    WITH course, user
    MATCH (course)<-[:BRANCH_DESCRIBE{userId: user.userId}]-(graph:Workspace)-[oldWork:WORK_ON]->(subject)
    RETURN graph
}
RETURN graph