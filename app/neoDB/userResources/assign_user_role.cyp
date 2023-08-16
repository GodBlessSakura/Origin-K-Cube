MATCH
(permission:Permission{role: $role}),
(user:User{userId: $userId})
WHERE NOT $REQUIRE_USER_VERIFICATION OR ($REQUIRE_USER_VERIFICATION AND user.verified)
MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user)
ON CREATE
SET
permission_grant.creationDate = datetime.transaction(),
permission_grant.message = $message
RETURN user, permission_grant, permission;