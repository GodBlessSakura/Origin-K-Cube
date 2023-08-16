MATCH (courseConcept:GraphConcept{name: $courseCode})
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.isInternal = $isInternal
RETURN course