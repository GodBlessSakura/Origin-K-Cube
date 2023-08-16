MATCH (concept:GraphConcept)
OPTIONAL MATCH (course:Course)-[:COURSE_DESCRIBE]->(concept:GraphConcept)
RETURN course, concept