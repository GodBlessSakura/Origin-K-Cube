MATCH (u)-[p]-() WITH type(p) AS RelationshipName, 
count(p) as RelationshipNumber 
RETURN RelationshipName, RelationshipNumber; 
