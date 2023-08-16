MATCH (user)-[:USER_OWN]->(overwritee{deltaGraphId: $overwriteeId})
WHERE NOT EXISTS((overwritee)<-[:PATCH]-())
WITH DISTINCT overwritee, user
CALL{
    WITH user
    MATCH (overwriter:Branch{deltaGraphId: $overwriterId}), (course:Course)
    WHERE toString(id(course)) = split($overwriterId,'.')[0]
    WITH 
        overwriter,
        user,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching
    WHERE        
        (overwriter.visibility = 4) OR
        (overwriter.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (overwriter.visibility = 2 AND isInstructor) OR
        (overwriter.visibility = 1 AND isTeaching) OR
        EXISTS((overwriter)<-[:USER_OWN]-(user))
    RETURN overwriter
UNION
    MATCH (overwriter:Trunk{deltaGraphId: $overwriterId})
    RETURN overwriter
}
WITH overwriter, overwritee, user
CREATE
    (overwritee)<-[:PATCH]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (branch)-[:BRANCH_PULL{increment: true}]->(overwriter)
SET 
    branch.visibility = 
        CASE overwritee.visibility
            WHEN null
            THEN 0
            ELSE overwritee.visibility
            END,
    branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(overwritee.deltaGraphId,'.')[0] + '.' + id(branch),
    branch.tag = $tag
WITH overwritee, branch
MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $overwriterId}]->(wt:GraphConcept)
WITH wr, wh, wt, branch, overwritee
CALL{
    WITH wr, wh, wt, branch, overwritee
    OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(wt)
    WITH
        wr, wh, wt, branch, overwritee,
        CASE sr
            WHEN null
            THEN {value: 'null'}
            ELSE sr
            END as sr
    WHERE
        wr.value <> sr.value AND
        NOT wr.value = false
    MERGE (wh)-[fr:DELTA_GRAPH_RELATIONSHIP{name: wr.name, deltaGraphId: branch.deltaGraphId}]-> (wt)
    SET
        fr.creationDate = wr.creationDate,
        fr.value = wr.value
    RETURN null
UNION
    WITH branch, overwritee
    MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(st:GraphConcept)
    MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: branch.deltaGraphId}]-> (st)
    ON CREATE SET
        fr.creationDate = sr.creationDate,
        fr.value = sr.value
    RETURN null
}
RETURN DISTINCT branch