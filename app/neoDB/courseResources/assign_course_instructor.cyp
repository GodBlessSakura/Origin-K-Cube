MATCH
    (operator:User{userId: $operatorId})-[:PRIVILEGED_OF]->(:Permission{canAssignCourse: true}),
    (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true}),
    (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MERGE (instructor)-[:USER_TEACH]->(course)