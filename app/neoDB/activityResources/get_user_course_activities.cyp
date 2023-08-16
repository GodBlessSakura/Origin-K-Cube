MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH
    (concept:GraphConcept)<-[:ACTIVITY_OF]-(activity:Activity)<-[:INSTRUCTOR_CREATE]-(user:User{userId: $userId}),
    (activity)-[:ATTRIBUTE_FROM]->(course)
RETURN activity, concept, user