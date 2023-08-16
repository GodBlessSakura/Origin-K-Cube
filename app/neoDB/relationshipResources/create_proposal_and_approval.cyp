MATCH (approver:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canApproveRelationship: true})
MERGE (r:GraphRelationship{name: $name})
MERGE (r)<-[:USER_PROPOSE]-(approver)
MERGE (r)<-[:USER_APPROVE]-(approver);