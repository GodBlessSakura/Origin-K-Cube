MATCH (:Course)<-[:TRUNK_DESCRIBE]-(activeTrunk)
WITH DISTINCT activeTrunk.deltaGraphId as activeDeltaGraphIds
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP]->(t:GraphConcept)
WHERE r.deltaGraphId in activeDeltaGraphIds
RETURN h.name, r.name, t.name, r.value , count(r.deltaGraphId) AS trunkVote