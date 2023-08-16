CALL{
    MATCH (branch:Branch)<-[:USER_OWN]-(owner_of_branch), (course:Course)
    WHERE split(branch.deltaGraphId,'.')[0] = toString(id(course))
    WITH branch, owner_of_branch, course
    CALL{
        WITH branch, owner_of_branch, course
        MATCH (user:User{userId: $userId})
        WITH 
            branch,
            user,
            owner_of_branch,
            EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
            EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
            EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching,
            EXISTS((branch)<-[:USER_OWN]-(user)) as isOwner
        WHERE
            (branch.visibility = 3 AND (isDLTC OR isInstructor)) OR
            (branch.visibility = 2 AND isInstructor) OR
            (branch.visibility = 1 AND isTeaching) OR
            isOwner
        RETURN DISTINCT branch AS deltaGraph, owner_of_branch as owner
    UNION
        WITH branch, owner_of_branch
        WITH branch, owner_of_branch
        WHERE branch.visibility = 4
        RETURN DISTINCT branch AS deltaGraph,owner_of_branch as owner
    }
    RETURN deltaGraph, owner
UNION
    MATCH (trunk:Trunk)
    WITH DISTINCT trunk
    RETURN DISTINCT trunk AS deltaGraph, null as owner
}
WITH deltaGraph, owner, collect(deltaGraph.deltaGraphId) as deltaGraphId
MATCH (h:GraphConcept{name: $h_name})-[r:DELTA_GRAPH_RELATIONSHIP{name: $r_name}]->(t:GraphConcept{name: $t_name})
WHERE r.deltaGraphId in deltaGraphId
RETURN r, deltaGraph, owner