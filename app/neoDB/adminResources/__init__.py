import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


class adminDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_all_except_credential(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = (
                "MATCH p = (h)-[r]->(t)"
                "WHERE 'Credential' NOT IN labels(h) AND 'Credential' NOT IN labels(t)"
                "RETURN p;"
            )
            result = tx.run(query)
            try:
                return result
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def readonly_query(self, query) -> bool:
        CUD_keywords = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE"]
        CUD_keywords = [keyword.strip() for keyword in CUD_keywords]
        CUD_keywords = [keyword.upper() for keyword in CUD_keywords]
        for keyword in CUD_keywords:
            if keyword in query.upper():
                return None

        fname = sys._getframe().f_code.co_name

        def _query(tx):
            result = tx.run(query)
            try:
                for record in result:
                    return record
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_role(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [dict(record["permission"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_user_role(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {"user": dict(record["user"].items()), "roles": record["roles"]}
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def user_statistic(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {"user": dict(record["user"].items()), "roles": record["roles"]}
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def deltaGraph_statistic(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {"user": dict(record["user"].items()), "roles": record["roles"]}
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def node_statistic(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "NodeType": record["NodeType"],
                        "NumberOfNodes": record["NumberOfNodes"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def edge_statistic(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [
                    {
                        "RelationshipName": record["RelationshipName"],
                        "RelationshipNumber": record["RelationshipNumber"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
