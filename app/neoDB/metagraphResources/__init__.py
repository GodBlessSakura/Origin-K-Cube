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
class metagraphDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_metagraph_concept(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [record["name"] for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_metagraph_triple(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
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

    def create_metagraph_triple(self, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, h_name=h_name, r_name=r_name, t_name=t_name)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def delete_metagraph_triple(self, h_name, r_name, t_name):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, h_name=h_name, r_name=r_name, t_name=t_name)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_metagraph_data(self, name, data):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name, data=data)
            try:
                return [
                    {
                        "h_name": record["h_name"],
                        "r_name": record["r_name"],
                        "t_name": record["t_name"],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_metagraph_data(self, name, data):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name, data=data)
            try:
                return [record["entity.metaData"] for record in result][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_metagraph_data(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return {record["entity.name"]: record["entity.metaData"] for record in result}

            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
