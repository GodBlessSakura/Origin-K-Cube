MATCH (approver:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canApproveRelationship: true})
MATCH (r:GraphRelationship{name: $name})
MERGE (r)<-[:USER_APPROVE]-(approver);