MATCH (:GraphConcept{name: $courseCode})<-[:COURSE_DESCRIBE]-(course)
RETURN course