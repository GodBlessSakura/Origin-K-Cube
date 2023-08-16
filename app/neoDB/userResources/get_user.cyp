MATCH (user:User {userId: $userId})
RETURN user;