MATCH (user:User{userId: $userId})
WITH DISTINCT user
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
WITH user, overwriter

MATCH (overwritee:Branch{deltaGraphId: $overwriteeId}), (course:Course)
    WHERE toString(id(course)) = split($overwriterId,'.')[0]
WITH 
    overwritee,
    course,
    user,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching
WHERE        
    (overwritee.visibility = 4) OR
    (overwritee.visibility = 3 AND (isDLTC OR isInstructor)) OR
    (overwritee.visibility = 2 AND isInstructor) OR
    (overwritee.visibility = 1 AND isTeaching) OR
    EXISTS((overwritee)<-[:USER_OWN]-(user))
CREATE
    (overwritee)<-[:FORK]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (branch)-[:BRANCH_PULL{increment: true}]->(overwriter)
SET 
    branch.visibility = 0,
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