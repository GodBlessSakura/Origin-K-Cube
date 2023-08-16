MATCH (:User{userId: $userId})-[:PRIVILEGED_OF]->(permissions:Permission)
RETURN permissions;