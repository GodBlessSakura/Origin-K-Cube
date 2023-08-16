MATCH (:GraphConcept{name: $name})<-[:COURSE_DESCRIBE]-(:Course)<-[:DRAFT_DESCRIBE]-(draft:Draft)<-[:USER_OWN]-(:User{userId: $userId})
RETURN draft