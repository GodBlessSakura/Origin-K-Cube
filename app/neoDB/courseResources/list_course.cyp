MATCH (course:Course{isInternal:false})-[:COURSE_DESCRIBE]->(courseConcept)
RETURN course,courseConcept