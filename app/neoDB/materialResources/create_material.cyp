MATCH (user:User{userId: $userId}), (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canWriteAllCourseMaterial: true})) or
    EXISTS((user)-[:USER_TEACH]->(course))
WITH DISTINCT user, course
MATCH (concept:GraphConcept{name: $name})
CREATE (concept)<-[:CONTENT_DESCRIBE]-(material:Material:GraphAttribute)<-[:INSTRUCTOR_CREATE]-(user)
MERGE (material)-[:ATTRIBUTE_FROM]->(course)
SET
    material.url = $url,
    material.desc = $desc
RETURN material, concept
