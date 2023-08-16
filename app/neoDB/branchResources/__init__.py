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
class branchDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_course_branch_edge(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "id": record["edges"].id,
                        "type": record["edges"].type,
                        "start": record["edges"].start_node.id,
                        "end": record["edges"].end_node.id,
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["edges"].items()
                        },
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_course_branch_node(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "id": record["nodes"].id,
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["nodes"].items()
                        },
                        "userId": record["userId"],
                        "isOwner": record["isOwner"],
                        "isExposed": record["isExposed"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def pull_as_fork(self, overwriterId, overwriteeId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                overwriterId=overwriterId,
                overwriteeId=overwriteeId,
                userId=userId,
                tag=tag,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def pull_as_patch(self, overwriterId, overwriteeId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                overwriterId=overwriterId,
                overwriteeId=overwriteeId,
                userId=userId,
                tag=tag,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    # not implemented
    # increment produce update summary, e.g. diff in number of triple
    def increment_pull_as_fork(self, overwriterId, overwriteeId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                overwriterId=overwriterId,
                overwriteeId=overwriteeId,
                userId=userId,
                tag=tag,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def increment_pull_as_patch(self, overwriterId, overwriteeId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                overwriterId=overwriterId,
                overwriteeId=overwriteeId,
                userId=userId,
                tag=tag,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_canPull(self, deltaGraphId, userId, canPull):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                canPull=canPull,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_visibility(self, deltaGraphId, userId, visibility):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                visibility=visibility,
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_canPullSummary(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
            )
            try:
                return [
                    {
                        "branch": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["branch"].items()
                        },
                        "course": dict(record["course"].items()),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
