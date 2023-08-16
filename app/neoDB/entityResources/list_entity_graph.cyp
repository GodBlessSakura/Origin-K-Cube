MATCH (course:Course{isInternal:false})
WITH DISTINCT course
CALL{
    WITH course
    MATCH (course)<-[:BRANCH_DESCRIBE]-(graph)<-[:USER_OWN]-(user:User)
    WHERE EXISTS((user)-[:USER_TEACH]->(course))
    RETURN graph.deltaGraphId as deltaGraphId, user.userId as userId
UNION
    WITH course
    MATCH (course)<-[:TRUNK_DESCRIBE]-(graph:Trunk)
    RETURN graph.deltaGraphId as deltaGraphId, null as userId
}
WITH deltaGraphId, course, userId
MATCH (concept:GraphConcept{name: $name})-[:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: deltaGraphId}]-()
RETURN DISTINCT course, userId

