MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH
    (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material)<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId}),
    (material)-[:ATTRIBUTE_FROM]->(course)
RETURN material, concept