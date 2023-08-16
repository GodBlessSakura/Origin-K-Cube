MATCH
    (trunk:Trunk),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE split(trunk.deltaGraphId,'.')[0] = toString(id(course))
WITH DISTINCT trunk, EXISTS((:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)) as isActive
RETURN trunk AS nodes, isActive
