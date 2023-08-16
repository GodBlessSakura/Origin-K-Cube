MATCH (branch:Branch{canPull: true}), (course:Course)
WHERE toString(id(course)) = split(branch.deltaGraphId,'.')[0]
RETURN branch, course