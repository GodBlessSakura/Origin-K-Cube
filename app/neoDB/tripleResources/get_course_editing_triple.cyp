MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}), (user:User{userId: $userId})
WITH course, user
MATCH (course)<-[:BRANCH_DESCRIBE{userId: user.userId}]-(branch:Branch)
WITH DISTINCT branch
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: branch.deltaGraphId}]->(t:GraphConcept)
RETURN h.name as h_name, r.name as r_name, t.name as t_name, r.value as r_value