MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (courseConcept:GraphConcept)<-[:COURSE_DESCRIBE]-(course:Course)<-[:DRAFT_DESCRIBE]-(draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner)
RETURN draft, courseConcept.name as root, course