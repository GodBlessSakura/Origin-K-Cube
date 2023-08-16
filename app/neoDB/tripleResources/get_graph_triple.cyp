MATCH (user:User{userId: $userId})
WITH user
CALL{
    WITH user
    MATCH (graph:Branch{deltaGraphId: $deltaGraphId}), (course:Course)
    WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
    WITH 
        graph,
        user,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching
    WHERE
        (graph.visibility = 4) OR
        (graph.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (graph.visibility = 2 AND isInstructor) OR
        (graph.visibility = 1 AND isTeaching) OR
        EXISTS((graph)<-[:USER_OWN]-(user))
        
    RETURN graph
UNION
    MATCH (graph:Trunk{deltaGraphId: $deltaGraphId})
    RETURN graph
}
WITH DISTINCT graph
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: graph.deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value