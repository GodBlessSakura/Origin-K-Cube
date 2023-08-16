MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
SET branch.canPull = $canPull,
    branch.canPullDate = datetime.transaction()
RETURN branch