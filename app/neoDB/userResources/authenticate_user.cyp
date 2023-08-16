MATCH (user:User{userId: $userId})-[:AUTHENTICATED_BY]->(password:Credential)
RETURN user, password.saltedHash as hash;