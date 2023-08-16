CALL{
    MATCH (graph:DeltaGraph)
    WHERE graph.deltaGraphId in $deltaGraphIds
    WITH graph
    CALL{
        WITH graph
        MATCH (user:User{userId: $userId}), (course:Course)
        WHERE toString(id(course)) = split(graph.deltaGraphId,'.')[0]
        WITH 
            graph,
            user,
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
        RETURN DISTINCT graph AS deltaGraph
    }
    RETURN deltaGraph
}
WITH collect(deltaGraph.deltaGraphId) as deltaGraphId
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP]->(t:GraphConcept)
WHERE r.deltaGraphId in deltaGraphId
RETURN h.name as h_name, r, t.name as t_name