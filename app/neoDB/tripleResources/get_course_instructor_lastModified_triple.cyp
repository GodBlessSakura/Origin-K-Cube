MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MATCH (user:User{userId: $userId})-[:USER_TEACH]->(course)
MATCH (workspace:Workspace)<-[:USER_OWN]-(user)
WHERE split(workspace.deltaGraphId,'.')[0] = toString(id(course))
WITH collect(workspace) as workspaces, max(workspace.lastModified) as lastModified, course, user
WITH [w IN workspaces WHERE w.lastModified = lastModified][0] as workspace, course, user
CALL{
    WITH workspace, course, user
    MATCH (workspace)-[oldWork:WORK_ON]->(subject)
    WITH DISTINCT workspace
    MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: workspace.deltaGraphId}]->(t:GraphConcept)
    RETURN h.name as h_name, r.name as r_name, t.name as t_name, r.value as r_value
UNION
    WITH workspace, course, user
    MATCH (workspace)-[oldWork:WORK_ON]->(subject)
    WITH DISTINCT workspace, subject
    OPTIONAL MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: workspace.deltaGraphId}]->(wt:GraphConcept)
    WITH wr, wh, wt, subject, workspace
    CALL{
        WITH wr, wh, wt, subject
        OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(wt)
        WITH
            wr, wh, wt, subject,
            CASE sr
                WHEN null
                THEN {value: 'null'}
                ELSE sr
                END as sr
        WHERE
            wr.value <> false AND
            NOT (
                wr.value = false AND 
                sr.value = 'null'
                )
        RETURN wh.name as h_name, wr.name as r_name, wt.name as t_name, wr.value as r_value
    UNION
        WITH workspace, subject
        MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(st:GraphConcept)
        WHERE not EXISTS((sh)-[:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: workspace.deltaGraphId}]->(st)) 
        RETURN sh.name as h_name, sr.name as r_name, st.name as t_name, sr.value as r_value
    }
    RETURN h_name, r_name, t_name, r_value
}
RETURN h_name, r_name, t_name, r_value