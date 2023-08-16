MATCH (owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})
WITH DISTINCT owner
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept:GraphConcept{name: $name})
CREATE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)
SET draft.draftId = owner.userId +. + replace(courseConcept.name,_) +. + replace($draftName,_),
draft.draftName = $draftName,
draft.creationDate = datetime.transaction(),
draft.lastModified = datetime.transaction(),
draft.status = 'unpublished'
RETURN draft;