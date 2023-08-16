MATCH (permission:Permission{role: 'restricted'})
CREATE (permission)<-[permission_grant:PRIVILEGED_OF]-(user:User {userId: $userId, userName: $userName, email: $email, verified: false})
-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash})
SET
password_set.creationDate = datetime.transaction(),
permission_grant.creationDate = datetime.transaction()
RETURN user;