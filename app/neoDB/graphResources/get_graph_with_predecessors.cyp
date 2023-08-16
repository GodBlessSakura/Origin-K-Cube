
CALL{        
    MATCH (:DeltaGraph{deltaGraphId: $deltaGraphId})-[:PATCH|FORK|TRUNK_PULL|BRANCH_PULL*]->(predecessors)
    RETURN predecessors as graph
UNION
    MATCH (graph:DeltaGraph{deltaGraphId: $deltaGraphId})
    RETURN graph
}
WITH graph
MATCH (user:User{userId: $userId}), (course:Course), (graph)<-[:USER_OWN]-(owner)
WHERE toString(id(course)) = split(graph.deltaGraphId,'.')[0]
WITH 
    graph,
    user,
    course,
    owner,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching,
    EXISTS((graph)<-[:USER_OWN]-(user)) as isOwner
WHERE
    (graph.visibility = 4) OR
    (graph.visibility = 3 AND (isDLTC OR isInstructor)) OR
    (graph.visibility = 2 AND isInstructor) OR
    (graph.visibility = 1 AND isTeaching) OR
    isOwner
MATCH (course)-[:COURSE_DESCRIBE]->(courseConcept)
RETURN DISTINCT graph, course, owner, courseConcept.name as courseCode