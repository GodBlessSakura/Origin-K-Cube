MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
SET branch.visibility = 
    CASE branch.visibility < toInteger($visibility)
        WHEN true THEN toInteger($visibility)
        ELSE branch.visibility
    END
WITH DISTINCT branch
OPTIONAL MATCH (ancestor)<-[:PATCH*]-(branch)
WITH DISTINCT ancestor, branch
SET ancestor.visibility = 
CASE ancestor.visibility < branch.visibility
    WHEN true THEN branch.visibility
    ELSE ancestor.visibility
END
RETURN branch