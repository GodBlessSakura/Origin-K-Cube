MATCH (user:User {userId: $userId})
MERGE (user)-[:REQUEST_TOKEN]->(token:ResetPasswordToken)
SET token.hash = $hash
RETURN user, token;