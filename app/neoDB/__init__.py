from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


class APIDriver:
    def __init__(self, uri, user, password):
        print("connect neo4j with: " + uri)
        if "neo4j+s" in uri:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        else:
            self.driver = GraphDatabase.driver(
                uri, auth=(user, password), encrypted=False
            )

        from .userResources import userDAO

        self.user = userDAO(driver=self.driver)

        from .courseResources import courseDAO

        self.course = courseDAO(driver=self.driver)

        from .adminResources import adminDAO

        self.admin = adminDAO(driver=self.driver)

        from .relationshipResources import relationshipDAO

        self.relationship = relationshipDAO(driver=self.driver)

        from .tripleResources import tripleDAO

        self.triple = tripleDAO(driver=self.driver)

        from .graphResources import graphDAO

        self.graph = graphDAO(driver=self.driver)

        from .entityResources import entityDAO

        self.entity = entityDAO(driver=self.driver)

        from .trunkResources import trunkDAO

        self.trunk = trunkDAO(driver=self.driver)

        from .branchResources import branchDAO

        self.branch = branchDAO(driver=self.driver)

        from .workspaceResources import workspaceDAO

        self.workspace = workspaceDAO(driver=self.driver)

        from .materialResources import materialDAO

        self.material = materialDAO(driver=self.driver)

        from .feedbackResources import feedbackDAO

        self.feedback = feedbackDAO(driver=self.driver)

        from .metagraphResources import metagraphDAO

        self.metagraph = metagraphDAO(driver=self.driver)

        from .activityResources import activityDAO

        self.activity = activityDAO(driver=self.driver)

    def close(self):
        self.driver.close()

    def init_neo4j(self):

        fname = sys._getframe().f_code.co_name
        query = cypher[fname + ".cyp"]
        queries = query.split(";")
        for query in queries:

            def _query(tx):
                result = tx.run(query)
                try:
                    return [record for record in result]
                except ServiceUnavailable as exception:
                    raise exception

            with self.driver.session() as session:
                session.write_transaction(_query)
