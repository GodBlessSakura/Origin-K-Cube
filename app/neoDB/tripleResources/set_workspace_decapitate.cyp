MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT workspace
MATCH (subject)<-[:WORK_ON]-(workspace)
MATCH (approved_r:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)
MERGE (h:GraphConcept{name: $h_name})
WITH workspace, subject, approved_r, h
CALL{
    WITH workspace, subject, approved_r, h
    MATCH (h) -[:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: subject.deltaGraphId, value: true}]-> (subject_t)
    MERGE (h) -[new_r:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: workspace.deltaGraphId}]-> (subject_t)
    SET
        new_r.creationDate = datetime.transaction(),
        new_r.value = false
    RETURN h.name as h_name, new_r.name as r_name, subject_t.name as t_name, new_r.value as r_value
union
    WITH workspace, subject, approved_r, h
    MATCH (h) -[r:DELTA_GRAPH_RELATIONSHIP{name: approved_r.name, deltaGraphId: workspace.deltaGraphId, value: true}]-> (t)
    WITH h, r, t, r.name as r_name
    DELETE r
    RETURN h.name as h_name, r_name, t.name as t_name, null as r_value
}
RETURN h_name, r_name, t_name, r_value