MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT workspace
MATCH (subject)<-[:WORK_ON]-(workspace)
MATCH (approved_r:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)
MERGE (h:GraphConcept{name: $h_name})
MERGE (t:GraphConcept{name: $t_name})
WITH workspace, subject, approved_r, h, t
OPTIONAL MATCH (h) -[r:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: workspace.deltaGraphId, value: true}]-> ()
DELETE r
WITH workspace, subject, approved_r, h, t
CALL{
    WITH workspace, subject, approved_r, h, t
    MATCH (h) -[:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: subject.deltaGraphId, value: true}]-> (subject_t)
    MERGE (h) -[new_r:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: workspace.deltaGraphId}]-> (subject_t)
    SET
        new_r.creationDate = datetime.transaction(),
        new_r.value = false
    RETURN null
union
    RETURN null
}
WITH workspace, approved_r, h, t
MERGE (h) -[exclusive_r:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: workspace.deltaGraphId}]-> (t)
SET
    workspace.lastModified = datetime.transaction(),
    exclusive_r.creationDate = datetime.transaction(),
    exclusive_r.value = $r_value
RETURN h.name, exclusive_r.name, t.name, exclusive_r.value;