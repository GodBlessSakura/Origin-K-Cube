MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WITH course
MATCH (user)-[:USER_FEEDBACK]->(feedback:Feedback)-[:FEEDBACK_ON]->(course)
RETURN user, feedback