MATCH (concept:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP]-()
WITH DISTINCT concept, split(r.deltaGraphId,'.')[0] as courseNodeId
MATCH (course:Course)
WHERE  toString(id(course)) = courseNodeId
WITH collect(course) as courses, concept, count(course) as count
WHERE count > 1
RETURN courses, concept