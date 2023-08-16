MATCH (permission:Permission{role: 'restricted'})
MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user:User {userId: $userId, email: $email, verified: true, type: 'oidc'})
SET
permission_grant.creationDate = datetime.transaction()
RETURN user;