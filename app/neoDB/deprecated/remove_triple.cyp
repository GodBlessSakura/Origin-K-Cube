MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT draft
MATCH (h:GraphConcept{name: $h_name})
MATCH (t:GraphConcept{name: $t_name})
MATCH (h) -[r:GRAPH_RELATIONSHIP{name: $r_name, draftId : draft.draftId}]-> (t)
WITH h.name as h_name, r.name as r_name, t.name as t_name, r, draft
DELETE r
SET draft.lastModified = datetime.transaction()
RETURN h_name, r_name, t_name;