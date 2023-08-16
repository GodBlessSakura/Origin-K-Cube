MATCH (proposer:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canWriteTeachingCourseBranch: true})
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})
WITH course, concept, proposer
MATCH (newConcept:GraphConcept{name: $newName})
MATCH (concept)-[:CONCEPT_DISAMBIGUATION_REPLACED]->(p:ConceptDisambiguationProposal{
    courseCode:$courseCode
})-[:CONCEPT_DISAMBIGUATION_REPLACING]->(newConcept)
MATCH (p)<-[up:USER_PROPOSE]-(proposer)
DELETE up