MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH DISTINCT workspace
OPTIONAL MATCH ()-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: workspace.deltaGraphId}]-> ()
DELETE r
DETACH DELETE workspace
RETURN workspace