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
class materialDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_a_user_material(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "concept": record["concept"]["name"],
                        "desc": record["material"]["desc"],
                        "url": record["material"]["url"],
                        "id": record["material"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_a_course_material(self, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode)
            try:
                return [
                    {
                        "user": record["user"]["userId"],
                        "concept": record["concept"]["name"],
                        "desc": record["material"]["desc"],
                        "url": record["material"]["url"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_material(self, courseCode, userId, name, url, desc):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                courseCode=courseCode,
                userId=userId,
                name=name,
                url=url,
                desc=desc,
            )
            try:
                return [
                    {
                        "concept": record["concept"]["name"],
                        "desc": record["material"]["desc"],
                        "url": record["material"]["url"],
                        "id": record["material"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_material(self, courseCode, userId, name, url, desc):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                courseCode=courseCode,
                userId=userId,
                name=name,
                url=url,
                desc=desc,
            )
            try:
                return [
                    {
                        "concept": record["concept"]["name"],
                        "desc": record["material"]["desc"],
                        "url": record["material"]["url"],
                        "id": record["material"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_material(self, id, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, id=id, userId=userId)
            try:
                return [
                    {
                        "desc": record["material"]["desc"],
                        "url": record["material"]["url"],
                        "id": record["material"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def materialCourseCount(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "course": dict(record["course"].items()),
                        "NumberOfMaterials": record["NumberOfMaterials"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
