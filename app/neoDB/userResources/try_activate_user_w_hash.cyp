MATCH (user:User)-[:ACTIVATE_BY]->(activation:ActivationToken{hash: $hash})
SET user.verified = true
RETURN user, activation;