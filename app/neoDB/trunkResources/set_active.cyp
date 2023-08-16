MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canWriteTrunk: true})
WITH user
MATCH (trunk:Trunk{deltaGraphId: $deltaGraphId})
WITH trunk
MATCH (course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH trunk, course
MATCH (course)<-[wasAstive:TRUNK_DESCRIBE]-(:Trunk)
DELETE wasAstive
MERGE (course)<-[:TRUNK_DESCRIBE]-(trunk)
RETURN trunk