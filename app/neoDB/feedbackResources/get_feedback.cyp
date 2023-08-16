MATCH (feedback:Feedback)
WHERE id(feedback) = toInteger($id)
WITH feedback
MATCH (user)-[:USER_FEEDBACK]->(feedback)
RETURN user, feedback