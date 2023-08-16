MATCH
    (operator:User{userId: $operatorId})-[:PRIVILEGED_OF]->(:Permission{canAssignCourse: true}),
    (instructor:User{userId: $userId}),
    (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}),
    (instructor)-[assignment:USER_TEACH]->(course)
DELETE assignment