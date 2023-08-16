MATCH (owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})
WITH DISTINCT owner
MATCH (course:Course)-[:COURSE_DESCRIBE]->(root:GraphConcept{name: $name})
CREATE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)
SET draft.draftId = owner.userId +. + replace(root.name,_) +. + replace($draftName,_),
draft.draftName = $draftName,
draft.creationDate = datetime.transaction(),
draft.lastModified = datetime.transaction(),
draft.status = 'unpublished'
WITH draft,root
MATCH (source:Draft{draftId: $draftId})-[:DRAFT_DESCRIBE]->()-[:COURSE_DESCRIBE]->(source_root:GraphConcept)
WITH draft, source, source_root, root
MATCH (h:GraphConcept)-[source_r:GRAPH_RELATIONSHIP{draftId: source.draftId}]->(t:GraphConcept)
WITH draft, source, source_root, root, h, source_r, t
CALL{
WITH draft, source, source_root, root, h, source_r, t
WITH draft, source, source_root, root, h, source_r, t
WHERE h <> source_root AND t <> source_root
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (t)
ON CREATE SET
r.creationDate = datetime.transaction()
RETURN NULL
UNION
WITH draft, source, source_root, root, h, source_r, t
WITH draft, source, source_root, root, h, source_r, t
WHERE h = source_root AND t <> root
MERGE (root) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (t)
ON CREATE SET
r.creationDate = datetime.transaction()
RETURN NULL
UNION
WITH draft, source, source_root, root, h, source_r, t
WITH draft, source, source_root, root, h, source_r, t
WHERE t = source_root AND h <> root
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (root)
ON CREATE SET
r.creationDate = datetime.transaction()
RETURN NULL
}
RETURN draft;