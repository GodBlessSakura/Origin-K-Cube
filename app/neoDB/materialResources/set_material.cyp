MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH
    (:GraphConcept{name: $name})<-[:CONTENT_DESCRIBE]-(material:Material)<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId}),
    (material)-[:ATTRIBUTE_FROM]->(course)
SET
    material.url = $url,
    material.desc = $desc
RETURN material, concept
