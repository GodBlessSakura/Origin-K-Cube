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
CREATE
    (graph)<-[:FORK]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (branch)<-[:WORK_ON]-(workspace:Workspace)<-[:USER_OWN]-(user)
SET
    
    branch.visibility = 0,
    branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(graph.deltaGraphId,'.')[0] + '.' + id(branch),
    branch.tag = $tag,
    workspace.creationDate = datetime.transaction(),
    workspace.lastModified = datetime.transaction(),
    workspace.deltaGraphId = split(graph.deltaGraphId,'.')[0] + '.' + id(workspace),
    workspace.tag = $w_tag
WITH branch, graph, workspace
CALL
{
    WITH branch, graph
    MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: graph.deltaGraphId}]->(st:GraphConcept)
    MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: branch.deltaGraphId}]-> (st)
    ON CREATE SET
        fr.creationDate = sr.creationDate,
        fr.value = sr.value
    RETURN null
UNION
    WITH workspace
    RETURN null
}
RETURN workspace.deltaGraphId as deltaGraphId;