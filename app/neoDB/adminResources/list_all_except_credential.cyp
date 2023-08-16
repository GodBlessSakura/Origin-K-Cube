MATCH p = (h)-[r]->(t)
WHERE 'Credential' NOT IN labels(h) AND 'Credential' NOT IN labels(t)
RETURN p;