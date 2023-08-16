OPTIONAL MATCH (n:User{userId: $userId})
RETURN n IS NOT NULL AS Predicate;