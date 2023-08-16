MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canGiveFeedback: true})
WITH DISTINCT user
MATCH (feedback:Feedback)
WHERE id(feedback) = toInteger($id)
WITH DISTINCT user, feedback
CREATE (user)-[reply:USER_REPLYING]->(feedback)
SET
    reply.creationDate = datetime.transaction(),
    reply.text = $text
RETURN reply
