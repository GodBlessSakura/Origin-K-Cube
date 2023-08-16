MATCH (user:User {userId: $userId})-[:REQUEST_TOKEN]->(token:ResetPasswordToken{hash: $hash})
MATCH (user)-[password_set:AUTHENTICATED_BY]->(credential:Credential)
SET
password_set.creationDate = datetime.transaction(),
credential.saltedHash =  $saltedHash
DETACH DELETE token
RETURN user;