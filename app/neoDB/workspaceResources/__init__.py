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
class workspaceDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_course_workspace_edge(self, courseCode, userId):
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

    def list_course_workspace_node(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "id": record["nodes"].id,
                        "canPatch": record["canPatch"],
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["nodes"].items()
                        },
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_workspace(self, deltaGraphId, tag, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, tag=tag, userId=userId)
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_repository(self, deltaGraphId, tag, userId, w_tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, tag=tag, userId=userId, w_tag=w_tag
            )
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_workspace(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            workspace = [
                dict(
                    dict(
                        {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["workspace"].items()
                        }.items()
                        | {
                            "isExposed": record["isExposed"],
                        }.items()
                    ).items(),
                    owner=dict(record["owner"].items()),
                    course=dict(record["course"].items()),
                )
                for record in result
            ][0]

            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_workspace_subject(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            workspace = [
                dict(
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["subject"].items()
                    }.items()
                    | {
                        "isPatchLeaf": record["isPatchLeaf"],
                        "isOwner": record["isOwner"],
                        "isExposed": record["isExposed"],
                        "isTeaching": record["isTeaching"],
                        "predecessor": record["predecessor"],
                    }.items(),
                    labels=list(record["subject"].labels),
                    courseCode=record["courseCode"],
                )
                for record in result
            ][0]

            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def commit_workspace_as_fork(self, deltaGraphId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId, tag=tag)
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

    def commit_workspace_as_patch(self, deltaGraphId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId, tag=tag)
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

    def sync_workspace(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def checkout_workspace(self, deltaGraphId, userId, checkout):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, userId=userId, checkout=checkout
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_from_import(self, deltaGraphId, triples, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            from ..relationshipResources import cypher as relationship_cypher
            from app.authorizer import permission_check

            regconized, privileged = permission_check(["canApproveRelationship"], True)
            print(privileged)
            if privileged:
                approved_relationship = tx.run(
                    relationship_cypher["list_approved_relationship.cyp"]
                )
                approved_relationship = [
                    record["r.name"] for record in approved_relationship
                ]
                unapproved_json_relationship = set(
                    [
                        triple["r_name"]
                        for triple in triples
                        if ("r_value" not in triple or triple["r_value"] == True)
                        and triple["r_name"] not in approved_relationship
                    ]
                )
                print(approved_relationship)
                print([triple for triple in triples])
                print(unapproved_json_relationship)
                for relationship in unapproved_json_relationship:
                    tx.run(
                        relationship_cypher["create_proposal_and_approval.cyp"],
                        userId=userId,
                        name=relationship,
                    )
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                triples=triples,
                userId=userId,
                tag=tag,
            )
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def update_from_import(self, deltaGraphId, triples, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            from ..relationshipResources import cypher as relationship_cypher
            from app.authorizer import permission_check

            regconized, privileged = permission_check(["canApproveRelationship"], True)
            if privileged:
                approved_relationship = tx.run(
                    relationship_cypher["list_approved_relationship.cyp"]
                )
                [record["r.name"] for record in result]
                unapproved_json_relationship = set(
                    [
                        triple["r_name"]
                        for triple in triples
                        if (triple["r_value"] == True or "r_value" not in triple)
                        and triple["r_name"] not in approved_relationship
                    ]
                )
                for relationship in unapproved_json_relationship:
                    tx.run(
                        relationship_cypher["create_proposal_and_approval .cyp"],
                        userId=userId,
                        name=relationship,
                    )
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                triples=triples,
                userId=userId,
            )
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

    def delete_workspace(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
            )
            try:
                return [
                    dict(
                        {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["workspace"].items()
                        }.items()
                    )
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user_course_lastModified(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            workspace = [
                dict(
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }.items()
                )
                for record in result
            ]
            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def commit_workspace_as_patch_n_expose(self, deltaGraphId, userId, tag):
        def _query(tx):
            commit_query = cypher["commit_workspace_as_patch.cyp"]
            from ..graphResources import cypher as graph_cypher

            expose_query = graph_cypher["set_isExposed.cyp"]
            result = tx.run(
                commit_query, deltaGraphId=deltaGraphId, userId=userId, tag=tag
            )
            try:
                branch = [record["branch"] for record in result][0]
            except Exception as exception:
                from ..resourcesGuard import InvalidRequest

                raise InvalidRequest("no meaningful edge update was found")
            result = tx.run(
                expose_query, deltaGraphId=branch["deltaGraphId"], userId=userId
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["graph"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            branch = session.write_transaction(_query)
            return branch

    def commit_workspace_as_fork_n_expose(self, deltaGraphId, userId, tag):
        def _query(tx):
            commit_query = cypher["commit_workspace_as_fork.cyp"]
            from ..graphResources import cypher as graph_cypher

            expose_query = graph_cypher["set_isExposed.cyp"]
            result = tx.run(
                commit_query, deltaGraphId=deltaGraphId, userId=userId, tag=tag
            )
            try:
                branch = [record["branch"] for record in result][0]
            except Exception as exception:
                from ..resourcesGuard import InvalidRequest

                raise InvalidRequest("no meaningful edge update was found")
            result = tx.run(
                expose_query, deltaGraphId=branch["deltaGraphId"], userId=userId
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["graph"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            branch = session.write_transaction(_query)
            return branch

    def rename_workspace(self, deltaGraphId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId, tag=tag)
            workspace = [
                dict(
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }.items()
                )
                for record in result
            ][0]
            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def assign_coauthor(self, deltaGraphId, userId, operatorId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, userId=userId, operatorId=operatorId
            )
            try:
                return True
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def unassign_coauthor(self, deltaGraphId, userId, operatorId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, userId=userId, operatorId=operatorId
            )
            try:
                return True
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_coauthor(self, deltaGraphId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId)
            try:
                return [
                    {
                        "user": dict(record["user"].items()),
                        "isCoauthoring": record["isCoauthoring"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def is_coauthor_or_owner(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [record for record in result][0]["is_coauthor_or_owner"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
