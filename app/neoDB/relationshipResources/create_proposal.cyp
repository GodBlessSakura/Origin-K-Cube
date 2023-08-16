MATCH (proposer:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canProposeRelationship: true})
MERGE (r:GraphRelationship{name:  $name})
MERGE (r)<-[:USER_PROPOSE]-(proposer);