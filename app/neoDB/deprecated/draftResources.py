from ..resourcesGuard import for_all_methods, reject_invalid
import sys


@for_all_methods(reject_invalid)
class draftResources:
    def __init__(self, driver):
        self.driver = driver

    def get_draft(self, draftId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, draftId=draftId, userId=userId)
            try:
                row = [record for record in result][0]
                draft = dict(row["draft"].items())
                draft["root"] = row["root"]
                draft["course"] = dict(row["course"].items())
                return draft
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_draft_status(self, draftId, userId, status):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                draftId=draftId,
                userId=userId,
                status=status,
            )
            try:
                return [record for record in result][0]["draft.status"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_draft(self, draftName, userId, name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            # if user have multiple permission that canCreateDraft and canOwnDraft, two identical user would be returned

            result = tx.run(
                query,
                draftName=draftName,
                userId=userId,
                name=name,
            )
            try:
                return dict([record for record in result][0]["draft"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_a_user_draft(self, userId, name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name, userId=userId)
            try:
                return [dict(record["draft"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def clone_draft(self, draftName, userId, name, draftId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                draftName=draftName,
                userId=userId,
                name=name,
                draftId=draftId,
            )
            try:
                return dict([record for record in result][0]["draft"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
