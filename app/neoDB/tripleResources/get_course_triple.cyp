MATCH (course:GraphConcept{name: $courseCode})
WITH course
MATCH (course)-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)
WITH DISTINCT trunk
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: trunk.deltaGraphId}]->(t:GraphConcept)
RETURN h.name as h_name, r.name as r_name, t.name as t_name, r.value as r_value
