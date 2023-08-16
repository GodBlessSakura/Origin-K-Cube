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
class feedbackDAO:
    def __init__(self, driver):
        self.driver = driver

    def create_feedback(self, courseCode, userId, title, text):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, courseCode=courseCode, userId=userId, title=title, text=text
            )
            try:
                return [
                    {
                        "title": record["feedback"]["title"],
                        "text": record["feedback"]["text"],
                        "id": record["feedback"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_reply(self, id, userId, text):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, id=id, userId=userId, text=text)
            try:
                return [
                    {"text": record["reply"]["text"], "id": record["reply"].id}
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_course_feedback(self, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode)
            try:
                return [
                    {
                        "user": record["user"]["userId"],
                        "title": record["feedback"]["title"],
                        "creationDate": str(
                            record["feedback"]["creationDate"].iso_format()
                        ),
                        "text": record["feedback"]["text"],
                        "id": record["feedback"].id,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_feedback(self, id):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, id=id)
            try:
                return [
                    dict(
                        {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["feedback"].items()
                        }.items()
                        | {"user": record["user"]["userId"]}.items()
                    )
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_reply(self, id):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, id=id)
            try:
                return [
                    dict(
                        {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["reply"].items()
                        }.items()
                        | {"user": record["user"]["userId"]}.items(),
                    )
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def discussionStatistic(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "course": dict(record["course"].items()),
                        "discussion": dict(
                            {
                                key: value
                                if not isinstance(value, DateTime)
                                else str(value.iso_format())
                                for key, value in record["discussion"].items()
                            }.items()
                        ),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
