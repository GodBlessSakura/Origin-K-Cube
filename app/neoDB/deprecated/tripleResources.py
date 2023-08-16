from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class tripleResources:
    def __init__(self, driver):
        self.driver = driver

    def get_draft_triple(self, draftId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, draftId=draftId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_triple(self, draftId, userId, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                draftId=draftId,
                userId=userId,
                h_name=h_name,
                r_name=r_name,
                t_name=t_name,
            )
            try:
                row = [record for record in result][0]
                return {
                    "h_name": row["h.name"],
                    "r_name": row["r.name"],
                    "t_name": row["t.name"],
                }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_triple(self, draftId, userId, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                draftId=draftId,
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

    def remove_unreachable_triple(self, draftId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, draftId=draftId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def aggregate_triple(self):
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
                        "draftVote": record["draftVote"],
                        "userVote": record["userVote"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
