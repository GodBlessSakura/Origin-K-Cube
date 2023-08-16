MATCH (material)<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
WHERE id(material) = toInteger($id)
DETACH DELETE material
RETURN material