CALL{
    MATCH (discussion:Feedback)-[:FEEDBACK_ON]->(course)
    return discussion, course
UNION
    MATCH ()-[reply:USER_REPLYING]->()-[:FEEDBACK_ON]->(course)
    return reply as discussion,  course
}
return discussion, course