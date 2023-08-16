MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})
OPTIONAL MATCH (concept)--(data:GraphAttribute)<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
WHERE EXISTS((data)-[:ATTRIBUTE_FROM]->(course))
RETURN DISTINCT concept, collect(data) as data