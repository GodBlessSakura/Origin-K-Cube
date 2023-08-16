MATCH (:GraphRelationship{name:  $name})<-[approval:USER_APPROVE]-(:User{userId: $userId})
DELETE approval