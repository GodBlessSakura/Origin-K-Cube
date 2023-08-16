MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})
MATCH (newConcept:GraphConcept{name: $newName})
MATCH
    (concept)-[:CONCEPT_DISAMBIGUATION_REPLACED]->
    (p:ConceptDisambiguationProposal{courseCode:$courseCode})
    -[:CONCEPT_DISAMBIGUATION_REPLACING]->(newConcept)
OPTIONAL MATCH (p)<-[up:USER_PROPOSE]-(proposer)
OPTIONAL MATCH (teacher)-[:USER_TEACH]->(course)
WITH count(DISTINCT teacher) AS nOfTeachers, count(DISTINCT proposer) AS nOfProposers, course, concept, newConcept, p
WHERE nOfProposers >= nOfTeachers
DETACH DELETE p
MERGE (concept)-[:DELTA_GRAPH_DISAMBIGUATION{
    creationDate: datetime.transaction(), userId: $userId, courseCode:$courseCode
}]->(newConcept)
WITH course, concept, newConcept
CALL{
    WITH course, concept, newConcept
    MATCH (concept)-[r:DELTA_GRAPH_RELATIONSHIP]->(theOther:GraphConcept)
    WHERE split(r.deltaGraphId,'.')[0] = toString(id(course))
    MERGE (newConcept)-[newR:DELTA_GRAPH_RELATIONSHIP{
        name: r.name, deltaGraphId: r.deltaGraphId
        }]->(theOther)
    SET
        newR.creationDate = CASE WHEN newR.creationDate > r.creationDate THEN newR.creationDate ELSE r.creationDate END,
        newR.value = r.value
    DELETE r
    RETURN null
UNION
    WITH course, concept, newConcept
    MATCH (concept)<-[r:DELTA_GRAPH_RELATIONSHIP]-(theOther:GraphConcept)
    WHERE split(r.deltaGraphId,'.')[0] = toString(id(course))
    MERGE (newConcept)<-[newR:DELTA_GRAPH_RELATIONSHIP{
        name: r.name, deltaGraphId: r.deltaGraphId
        }]-(theOther)
    SET
        newR.creationDate = CASE WHEN newR.creationDate > r.creationDate THEN newR.creationDate ELSE r.creationDate END,
        newR.value = r.value
    DELETE r
    RETURN null
UNION
    WITH concept, newConcept, course
    MATCH (concept)<-[rs:ACTIVITY_OF]-(oldActivity:Activity)-[:ATTRIBUTE_FROM]->(course), (user:User{userId: $userId})
    MERGE (newConcept)<-[:ACTIVITY_OF]-(newActivity:Activity:GraphAttribute{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(user)
    MERGE (newActivity)-[:ATTRIBUTE_FROM]->(course)
    SET
        newActivity.desc = oldActivity.desc,
        newActivity.week = oldActivity.week
    RETURN null
UNION
    WITH concept, newConcept, course
    MATCH (concept)<-[rs:CONTENT_DESCRIBE]-(attr:Material)-[:ATTRIBUTE_FROM]->(course)
    WITH newConcept, collect(rs) as rs, attr
    FOREACH (r in rs |
        MERGE (newConcept)<-[:CONTENT_DESCRIBE]-(attr)
        DELETE r
    )
    RETURN null
}
RETURN newConcept as concept