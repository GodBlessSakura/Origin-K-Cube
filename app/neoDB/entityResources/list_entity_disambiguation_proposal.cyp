
MATCH (user:User{userId: $userId}) with user
MATCH (concept)-[:CONCEPT_DISAMBIGUATION_REPLACED]->(proposal:ConceptDisambiguationProposal)-[:CONCEPT_DISAMBIGUATION_REPLACING]->(newConcept)
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: proposal.courseCode})
OPTIONAL MATCH (proposers:User)-[:USER_PROPOSE]->(proposal)
OPTIONAL MATCH (teacher)-[:USER_TEACH]->(course)
RETURN concept, newConcept, proposal, count(distinct teacher) AS nOfTeachers, count(distinct proposers) AS nOfProposers, user IN collect(proposers) AS amIProposing