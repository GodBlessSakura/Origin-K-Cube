MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner:User{userId: $userId})
WITH DISTINCT draft
SET draft.status = $status
RETURN draft.status;