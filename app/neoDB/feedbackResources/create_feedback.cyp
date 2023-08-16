MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canGiveFeedback: true})
WITH DISTINCT user
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MERGE (user)-[:USER_FEEDBACK]->(feedback:Feedback)-[:FEEDBACK_ON]->(course)
SET
    feedback.creationDate = datetime.transaction(),
    feedback.title = $title,
    feedback.text = $text
RETURN feedback
