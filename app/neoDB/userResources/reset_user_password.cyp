MATCH (user:User {userId: $userId})-[password_set:AUTHENTICATED_BY]->(credential:Credential)
SET
password_set.creationDate = datetime.transaction(),
credential.saltedHash =  $saltedHash
RETURN user;