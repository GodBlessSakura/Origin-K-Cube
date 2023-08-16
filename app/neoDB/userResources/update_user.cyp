MATCH (user:User {userId: $userId})
WHERE user.type <> 'oidc'
SET
user.verified = CASE user.email = $email
    WHEN true THEN CASE EXISTS(user.verified)
        WHEN true THEN user.verified
        ELSE false
        END 
    ELSE false
    END,
user.userName = $userName,
user.verified = CASE
    WHEN user.email = $email THEN user.verified
    ELSE false END,
user.email = $email
RETURN user;