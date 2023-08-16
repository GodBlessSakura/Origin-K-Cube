MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner)
SET workspace.tag = $tag
RETURN workspace