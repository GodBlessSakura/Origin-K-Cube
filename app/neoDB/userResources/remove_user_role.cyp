MATCH (permission:Permission{role: $role})<-[permission_grant:PRIVILEGED_OF]-(user:User{userId: $userId})
DELETE permission_grant
RETURN user, permission_grant, permission;