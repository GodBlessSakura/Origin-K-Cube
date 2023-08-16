MATCH (user:User{userId: $userId}) with user
MATCH (r:GraphRelationship)
OPTIONAL MATCH (proposers:User)-[:USER_PROPOSE]->(r)
OPTIONAL MATCH (r)<-[:USER_APPROVE]-(approvers:User)
RETURN r.name, count(distinct proposers) as nOfProposers, user IN collect(proposers) as amIProposing, count(distinct approvers) as nOfApprovers, user IN collect(approvers) as amIApproving