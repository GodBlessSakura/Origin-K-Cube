MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH
    (concept:GraphConcept)<-[:ACTIVITY_OF]-(courseEvent:CourseEvent)<-[:INSTRUCTOR_CREATE]-(user:User{userId: $userId}),
    (courseEvent)-[:ATTRIBUTE_FROM]->(course)
RETURN courseEvent, concept, user