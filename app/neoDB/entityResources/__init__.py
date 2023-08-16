from neo4j.time import DateTime
from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class entityDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_entity(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "course": dict(record["course"].items())
                        if record["course"] is not None
                        else None,
                        "concept": dict(record["concept"].items()),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_entity_graph(self, name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name)
            try:
                return [
                    {
                        "course": dict(record["course"].items()),
                        "userId": record["userId"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_mutual_entity(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "courses": [dict(course) for course in record["courses"]],
                        "concept": dict(record["concept"].items()),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user_course_entity(self, name, userId, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name, userId=userId, courseCode=courseCode)
            try:
                return [
                    {
                        "concept": dict(record["concept"].items()),
                        "data": [
                            dict(
                                {
                                    key: value
                                    if not isinstance(value, DateTime)
                                    else str(value.iso_format())
                                    for key, value in data.items()
                                }.items(),
                                labels=list(data.labels),
                                id=data.id,
                            )
                            for data in record["data"]
                        ],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def entity_disambiguation(self, name, courseCode, newName, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            test = tx.run(
                "MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})"
                "MATCH (newConcept:GraphConcept{name: $newName})"
                "MATCH"
                "(concept)-[:CONCEPT_DISAMBIGUATION_REPLACED]->"
                "(p:ConceptDisambiguationProposal{courseCode:$courseCode})"
                "-[:CONCEPT_DISAMBIGUATION_REPLACING]->(newConcept)"
                "OPTIONAL MATCH (p)<-[:USER_PROPOSE]-(proposer)"
                "OPTIONAL MATCH (teacher)-[:USER_TEACH]->(course)"
                "\n"
                "WITH count(DISTINCT teacher) AS nOfTeachers, count(DISTINCT proposer) AS nOfProposers"
                "\n"
                "RETURN nOfTeachers, nOfProposers",
                name=name,
                courseCode=courseCode,
                newName=newName,
                userId=userId,
            )
            try:
                oracle = [record for record in test][0]
                print(oracle)
                if oracle["nOfProposers"] < oracle["nOfTeachers"]:
                    from ..resourcesGuard import InvalidRequest

                    raise InvalidRequest(
                        "Not all instructors of this course agree this disambiguation"
                    )
            except Exception as exception:
                raise exception
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, name=name, courseCode=courseCode, newName=newName, userId=userId
            )
            try:
                return [
                    {
                        "concept": dict(record["concept"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_entity_disambiguation_proposal(self, name, courseCode, newName, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, name=name, courseCode=courseCode, newName=newName, userId=userId
            )
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_entity_disambiguation_proposal(self, name, courseCode, newName, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, name=name, courseCode=courseCode, newName=newName, userId=userId
            )
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_entity_disambiguation_proposal(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            try:
                return [
                    {
                        "concept": dict(record["concept"].items()),
                        "newConcept": dict(record["newConcept"].items()),
                        "proposal": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["proposal"].items()
                        },
                        "nOfProposers": record["nOfProposers"],
                        "nOfTeachers": record["nOfTeachers"],
                        "amIProposing": record["amIProposing"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
