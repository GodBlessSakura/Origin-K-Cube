MATCH (entity:GraphConcept{name: $name})
set entity.metaData = $data
return entity, entity.metaData