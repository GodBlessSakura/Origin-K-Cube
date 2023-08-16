from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class tripleDAO:
    def __init__(self, driver):
        self.driver = driver

    def get_workspace_triple(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                        "r_value": record["r.value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_workspace_triple(
        self, deltaGraphId, userId, h_name, r_name, t_name, r_value
    ):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
                t_name=t_name,
                r_value=r_value,
            )
            try:
                row = [record for record in result][0]
                return {
                    "h_name": row["h.name"],
                    "r_name": row["r.name"],
                    "t_name": row["t.name"],
                    "r_value": row["r.value"],
                }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_workspace_exclusive_head_triple(
        self, deltaGraphId, userId, h_name, r_name, t_name, r_value
    ):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
                t_name=t_name,
                r_value=r_value,
            )
            try:
                row = [record for record in result][0]
                return {
                    "h_name": row["h.name"],
                    "r_name": row["exclusive_r.name"],
                    "t_name": row["t.name"],
                    "r_value": row["exclusive_r.value"],
                }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_workspace_triple(self, deltaGraphId, userId, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
                t_name=t_name,
            )
            try:
                row = [record for record in result][0]
                return {
                    "h_name": row["h_name"],
                    "r_name": row["r_name"],
                    "t_name": row["t_name"],
                }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_unreachable_triple(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                triples = [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
                # if len(triples) == 0:
                #     from ..resourcesGuard import InvalidRequest
                #     raise InvalidRequest("no unreachable edge was found")
                return triples
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_workspace_subject_triple(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                        "r_value": record["r.value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_graph_triple(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                        "r_value": record["r.value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_course_triple(self, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_course_instructor_triple(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            result = tx.run(
                "MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})"
                "MATCH (user:User{userId: $userId})-[:USER_TEACH]->(course)"
                "RETURN user.userId as userId",
                courseCode=courseCode,
                userId=userId,
            )
            try:
                _ = [record["userId"] for record in result][0]
            except Exception as exception:
                from ..resourcesGuard import InvalidRequest
                from flask import g

                if g.user["userId"] == userId:
                    raise InvalidRequest("You are not on-duty for course " + courseCode)
                raise InvalidRequest("This instructor is not teaching this course")
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_course_instructor_lastModified_triple(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            result = tx.run(
                "MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})"
                "MATCH (user:User{userId: $userId})-[:USER_TEACH]->(course)"
                "RETURN user.userId as userId",
                courseCode=courseCode,
                userId=userId,
            )
            try:
                _ = [record["userId"] for record in result][0]
            except Exception as exception:
                from ..resourcesGuard import InvalidRequest
                from flask import g

                if g.user["userId"] == userId:
                    raise InvalidRequest("You are not on-duty for course " + courseCode)
                raise InvalidRequest("This instructor is not teaching this course")
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_course_editing_triple(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            result = tx.run(
                "MATCH (:GraphConcept{name: $courseCode})<-[:COURSE_DESCRIBE]-(course)<-[:BRANCH_DESCRIBE{userId: $userId}]-(branch:Branch)"
                "RETURN branch",
                courseCode=courseCode,
                userId=userId,
            )
            try:
                _ = [record["branch"] for record in result][0]
            except Exception as exception:
                from ..resourcesGuard import InvalidRequest

                raise InvalidRequest("You never expose any graph")
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_aggregated_triple(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                        "r_value": record["r.value"],
                        "trunkVote": record["trunkVote"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_workspace_decapitate(self, deltaGraphId, userId, h_name, r_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
            )
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                        "r_value": record["r_value"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_graph_history_triple(self, userId, deltaGraphId):
        from ..graphResources import cypher as graph_cypher

        fname = sys._getframe().f_code.co_name

        def _query(tx):
            result = tx.run(
                graph_cypher["get_graph_with_predecessors.cyp"],
                userId=userId,
                deltaGraphId=deltaGraphId,
            )
            from neo4j.time import DateTime

            deltaGraph = [
                dict(
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["graph"].items()
                    }.items()
                    | record["course"].items()
                    | record["owner"].items(),
                    labels=list(record["graph"].labels),
                    courseCode=record["courseCode"],
                )
                for record in result
            ]
            deltaGraphIds = [graph["deltaGraphId"] for graph in deltaGraph]
            triples = tx.run(
                cypher["get_graphs_triple.cyp"],
                userId=userId,
                deltaGraphIds=deltaGraphIds,
            )

            try:
                return {
                    "triples": [
                        {
                            "h_name": record["h_name"],
                            "t_name": record["t_name"],
                            "r": {
                                key: value
                                if not isinstance(value, DateTime)
                                else str(value.iso_format())
                                for key, value in record["r"].items()
                            },
                        }
                        for record in triples
                    ],
                    "graphs": deltaGraph,
                }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_triple_history(self, userId, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
                t_name=t_name,
            )
            from neo4j.time import DateTime

            try:
                return [
                    {
                        "relationship": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["r"].items()
                        },
                        "deltaGraph": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["deltaGraph"].items()
                        },
                        "ownerId": dict(record["owner"].items())["userId"]
                        if record["owner"]
                        else None,
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
