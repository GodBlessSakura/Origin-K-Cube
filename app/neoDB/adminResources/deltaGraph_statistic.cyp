CALL{
    MATCH (n) RETURN labels(n) AS NodeType, count(n) AS NumberOfNodes;
UNION
    MATCH (u)-[p]-() WITH type(p) AS RelationshipName, 
    count(p) as RelationshipNumber 
    RETURN RelationshipName, RelationshipNumber; 
}
RETURN *