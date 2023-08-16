MATCH (feedback:Feedback)
WHERE id(feedback) = toInteger($id)
WITH feedback
MATCH (user)-[reply:USER_REPLYING]->(feedback)
RETURN user, reply