import os

# basedir = os.path.abspath(".")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY = "Hard to guess string"
    DATABASE_ADDRESS = "bolt://117.50.175.233:7687"
    DATABASE = "neo4j"
    DATABASE_PASSWORD = "@XQ6o7l9"
    REQUIRE_USER_VERIFICATION = True

class standaloneConfig(Config):
    REQUIRE_USER_VERIFICATION = False
    DATABASE_ADDRESS = "bolt://neo4j:7687"


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    TESTING = False


config = {
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
    "productin": ProductionConfig(),
    "default": DevelopmentConfig(),
    "standalone": standaloneConfig()
}
