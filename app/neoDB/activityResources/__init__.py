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
class activityDAO:
    def __init__(self, driver):
        self.driver = driver
    
    def get_user_course_activities(self, userId, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, courseCode=courseCode, userId=userId
            )
            try:
                return [
                    {
                        "name": record["concept"]["name"],
                        "desc": record["activity"]["desc"],
                        "week": record["activity"]["week"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
        
    def get_department_course_activities(self, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, courseCode=courseCode
            )
            try:
                return [
                    {
                        "name": record["concept"]["name"],
                        "desc": record["activity"]["desc"],
                        "week": record["activity"]["week"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_user_course_activities(self, userId, courseCode, name, week, desc):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, courseCode=courseCode, userId=userId, name= name, week=week, desc=desc
            )
            try:
                return [
                    {
                        "desc": record["activity"]["desc"],
                        "week": record["activity"]["week"],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
        
    def set_department_course_activities(self, userId, courseCode, name, week, desc):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, courseCode=courseCode, userId=userId, name= name, week=week, desc=desc
            )
            try:
                return [
                    {
                        "desc": record["activity"]["desc"],
                        "week": record["activity"]["week"],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    