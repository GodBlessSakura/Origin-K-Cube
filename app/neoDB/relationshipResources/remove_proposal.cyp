MATCH (:GraphRelationship{name:  $name})<-[proposal:USER_PROPOSE]-(:User{userId: $userId})
DELETE proposal