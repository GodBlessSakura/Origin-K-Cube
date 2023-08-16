MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH DISTINCT workspace
MATCH (approved_graph_relationship:GraphRelationship)<-[:USER_APPROVE]-(:User)
WITH DISTINCT collect(approved_graph_relationship.name) as approved_graph_relationship_name, workspace
UNWIND [triple IN $triples WHERE triple.r_name IN approved_graph_relationship_name] as triple 
WITH DISTINCT workspace, triple
MERGE (h:GraphConcept{name: triple.h_name})
MERGE (t:GraphConcept{name: triple.t_name})
MERGE (h)-[r:DELTA_GRAPH_RELATIONSHIP{name: triple.r_name, deltaGraphId: workspace.deltaGraphId}]->(t)
SET
    r.creationDate = datetime.transaction(),
    r.value = CASE triple.r_value
        WHEN null
        THEN true
        ELSE triple.r_value
        END
SET workspace.lastModified = datetime.transaction()
RETURN h.name, r.name, t.name, r.value;