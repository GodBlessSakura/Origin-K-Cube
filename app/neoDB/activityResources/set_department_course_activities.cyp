MATCH (user:User{userId: $userId}), (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canWriteAllCourseMaterial: true})) or
    EXISTS((user)-[:USER_TEACH]->(course)) or
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role: "DLTC"}))
WITH DISTINCT user, course
MERGE (concept:GraphConcept{name: $name})
MERGE (concept)<-[:ACTIVITY_OF]-(activity:Activity:GraphAttribute{courseNodeId: id(course)})<-[old_create:DLTC_CREATE]-(:User)
// unique id is needed for activity beacuse we are using stupid merge
MERGE (activity)-[:ATTRIBUTE_FROM]->(course)
DELETE old_create
MERGE (activity)<-[:DLTC_CREATE]-(user)
SET
    activity.desc = $desc,
    activity.week = $week
RETURN activity