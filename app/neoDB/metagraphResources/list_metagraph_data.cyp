MATCH (entity:GraphConcept)
WHERE EXISTS(entity.metaData)
RETURN entity.name, entity.metaData