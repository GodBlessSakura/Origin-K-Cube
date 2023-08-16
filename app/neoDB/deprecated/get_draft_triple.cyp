MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner)
WITH DISTINCT draft
MATCH (h:GraphConcept)-[r:GRAPH_RELATIONSHIP{draftId: $draftId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name;