MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT workspace
MATCH (subject)<-[:WORK_ON]-(workspace)
MATCH (course:Course)-[:COURSE_DESCRIBE]->(root)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH workspace, root, subject
CALL{
    WITH workspace, root
    OPTIONAL MATCH reachable=(root)-[:DELTA_GRAPH_RELATIONSHIP*{deltaGraphId : workspace.deltaGraphId, value: true}]-(:GraphConcept)
    UNWIND (
        CASE reachable
            WHEN null THEN [null]
            ELSE relationships(reachable)
        END) AS reachable_relationships
    WITH collect(id(reachable_relationships)) AS reachable_id, workspace
    MATCH (h)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId : workspace.deltaGraphId, value: true}]->(t)
    WHERE NOT id(r) IN reachable_id
    WITH h, t, r, workspace, null as r_value, r.name as r_name
    DELETE r
    RETURN h.name AS h_name, r_name, t.name AS t_name, r_value
UNION
    WITH subject, root, workspace
    OPTIONAL MATCH reachable=(root)-[:DELTA_GRAPH_RELATIONSHIP*{deltaGraphId : subject.deltaGraphId, value: true}]-(:GraphConcept)
    UNWIND (
        CASE reachable
            WHEN null THEN [null]
            ELSE relationships(reachable)
        END) AS reachable_relationships
    WITH collect(id(reachable_relationships)) AS reachable_id, subject, workspace
    MATCH (h)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId : subject.deltaGraphId, value: true}]->(t)
    WHERE NOT id(r) IN reachable_id
    WITH h, t, r.name as r_name, workspace    
    MERGE (h) -[r:DELTA_GRAPH_RELATIONSHIP{name: r_name, deltaGraphId: workspace.deltaGraphId}]-> (t)
    ON CREATE SET
        r.creationDate = datetime.transaction(),
        r.value = false
    RETURN h.name AS h_name, r.name AS r_name, t.name AS t_name, r.value as r_value
}
SET workspace.lastModified = datetime.transaction()
RETURN h_name, r_name, t_name, r_value;