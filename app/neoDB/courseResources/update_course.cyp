MATCH (courseConcept:GraphConcept{name: $courseCode})
WITH courseConcept
CALL{
    WITH courseConcept
    WITH courseConcept
    WHERE NOT EXISTS(()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $name}))
    RETURN null
UNION
    WITH courseConcept
    WITH courseConcept
    WHERE courseConcept.name = $name
    RETURN null
}
WITH DISTINCT courseConcept
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET courseConcept.name = $name, course.name = $name
SET course.imageURL = $imageURL, course.courseName = $courseName
RETURN course
