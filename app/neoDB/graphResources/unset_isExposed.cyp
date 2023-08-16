MATCH (graph{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WHERE graph:Branch OR graph:Workspace
WITH graph
MATCH(course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH graph, course
MATCH (course)<-[wasExposed:BRANCH_DESCRIBE{userId: $userId}]-(graph)
DELETE wasExposed
RETURN graph