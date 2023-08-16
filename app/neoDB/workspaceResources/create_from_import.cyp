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
        EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching,
        EXISTS((graph)<-[:USER_OWN]-(user)) as isOwner
    WHERE        
        (graph.visibility = 4) OR
        (graph.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (graph.visibility = 2 AND isInstructor) OR
        (graph.visibility = 1 AND isTeaching) OR
        isOwner
    RETURN graph, isOwner
UNION
    MATCH (graph:Trunk{deltaGraphId: $deltaGraphId})
    RETURN graph, false as isOwner
}
CREATE (graph)<-[:WORK_ON]-(workspace:Workspace)<-[:USER_OWN]-(user)
SET
    workspace.creationDate = datetime.transaction(),
    workspace.lastModified = datetime.transaction(),
    workspace.deltaGraphId = split(graph.deltaGraphId,'.')[0] + '.' + id(workspace),
    workspace.tag = $tag
WITH workspace
MATCH (approved_graph_relationship:GraphRelationship)<-[:USER_APPROVE]-(:User)
WITH workspace, collect(approved_graph_relationship.name) as approved_graph_relationship_name
FOREACH(triple IN [triple IN $triples WHERE triple.r_name IN approved_graph_relationship_name] | 
    MERGE (h:GraphConcept{name: triple.h_name})
    MERGE (t:GraphConcept{name: triple.t_name})
    MERGE (h)-[r:DELTA_GRAPH_RELATIONSHIP{name: triple.r_name, deltaGraphId: workspace.deltaGraphId}]->(t)
    SET
        r.creationDate = datetime.transaction(),
        r.value = CASE triple.r_value
            WHEN null
            THEN true
            ELSE triple.r_value
            END
)
SET workspace.lastModified = datetime.transaction()
RETURN workspace.deltaGraphId as deltaGraphId;