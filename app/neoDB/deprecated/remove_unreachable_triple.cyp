MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT draft
MATCH (root:GraphConcept)<-[:COURSE_DESCRIBE]-(:Course)<-[:DRAFT_DESCRIBE]-(draft:Draft)
WITH draft, root
MATCH reachable=(root)-[:GRAPH_RELATIONSHIP*{draftId : draft.draftId}]-(:GraphConcept)
UNWIND relationships(reachable) AS reachable_relationships
WITH collect(id(reachable_relationships)) as reachable_id, draft
MATCH (h)-[r:GRAPH_RELATIONSHIP{draftId : draft.draftId}]->(t)
WHERE NOT id(r) IN reachable_id
WITH collect(h.name) as h_name, collect(r.name) as r_name, collect(t.name) as t_name, r, draft
DELETE r
SET draft.lastModified = datetime.transaction()
RETURN h_name, r_name, t_name;
                ]