MATCH (user:User)
OPTIONAL MATCH (user)-[:PRIVILEGED_OF]->(permission:Permission)
RETURN user, collect(permission.role) as roles