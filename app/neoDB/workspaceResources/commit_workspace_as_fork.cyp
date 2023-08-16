MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH DISTINCT workspace, user
MATCH (subject)<-[oldWork:WORK_ON]-(workspace)
DELETE oldWork
CREATE
    (subject)<-[:FORK]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (branch)<-[:WORK_ON]-(workspace)
SET 
    branch.visibility = 0,
    branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(subject.deltaGraphId,'.')[0] + '.' + id(branch),
    branch.tag = $tag
WITH subject, branch
MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $deltaGraphId}]->(wt:GraphConcept)
WITH wr, wh, wt, branch, subject
CALL{
    WITH wr, wh, wt, branch, subject
    OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(wt)
    WITH
        wr, wh, wt, branch, subject,
        CASE sr
            WHEN null
            THEN {value: 'null'}
            ELSE sr
            END as sr
    WHERE
        wr.value <> sr.value AND
        NOT (
            wr.value = false AND 
            sr.value = 'null'
            )
    MERGE (wh)-[fr:DELTA_GRAPH_RELATIONSHIP{name: wr.name, deltaGraphId: branch.deltaGraphId}]-> (wt)
    SET
        fr.creationDate = wr.creationDate,
        fr.value = wr.value
    DELETE wr
    RETURN null
UNION
    WITH branch, subject
    MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(st:GraphConcept)
    MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: branch.deltaGraphId}]-> (st)
    ON CREATE SET
        fr.creationDate = sr.creationDate,
        fr.value = sr.value
    RETURN null
}
RETURN DISTINCT branch