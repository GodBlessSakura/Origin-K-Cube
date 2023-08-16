MATCH
    (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true}),
    (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MERGE (instructor)-[:USER_TEACH]->(course)