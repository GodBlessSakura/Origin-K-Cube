MATCH (user:User {userId: $userId})
MERGE (user)-[:ACTIVATE_BY]->(activation:ActivationToken)
SET activation.hash = $hash, activation.email = user.email
RETURN activation;