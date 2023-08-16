MATCH
    (nodes:Trunk),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE split(nodes.deltaGraphId,'.')[0] = toString(id(course))
WITH DISTINCT nodes
CALL{
    WITH nodes
    MATCH (nodes)-[edges:PATCH|FORK]->(:Trunk)
    RETURN edges
UNION
    WITH nodes
    MATCH (:Trunk)-[edges:PATCH|FORK]->(nodes)
    RETURN edges
UNION
    WITH nodes
    MATCH (nodes)-[edges:TRUNK_PULL|BRANCH_PULL]->(:Branch)
    RETURN edges
}
RETURN DISTINCT edges as edges
