MATCH (selected_draft:Draft{status: 'published'})<-[:USER_OWN]-(owner:User)
WITH selected_draft.draftId as published_id, owner.userId as userId
WITH published_id, userId
MATCH (h:GraphConcept)-[r:GRAPH_RELATIONSHIP]->(t:GraphConcept)
WHERE r.draftId in published_id
RETURN h.name, r.name, t.name , count(distinct published_id) AS draftVote, count(distinct userId) AS userVote