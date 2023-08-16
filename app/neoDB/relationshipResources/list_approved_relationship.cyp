MATCH (r:GraphRelationship)<-[:USER_APPROVE]-(approvers:User)
RETURN DISTINCT r.name