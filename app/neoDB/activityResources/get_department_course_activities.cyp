MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (course)<-[:TRUNK_DESCRIBE]-(trunk)

MATCH
    (concept:GraphConcept)<-[:ACTIVITY_OF]-(activity:Activity)<-[:DLTC_CREATE]-(),
    (activity)-[:ATTRIBUTE_FROM]->(course)
RETURN activity, concept