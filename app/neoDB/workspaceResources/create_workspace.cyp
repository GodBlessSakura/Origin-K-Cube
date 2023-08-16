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
RETURN workspace.deltaGraphId as deltaGraphId;