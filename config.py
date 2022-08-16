from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class ProductionConfiguration:
    FLASK_ENV = "ProductionConfiguration"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class DevelopmentConfiguration:
    FLASK_ENV = "DevelopmentConfiguration"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestingConfiguration:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}")


def create_app(configuration=None):
    app = Flask(__name__)
    configuration = configuration if configuration else config("CONFIGURATION")
    app.config.from_object(configuration)

    api = Api(app)
    migrate = Migrate(app, db)
    db.init_app(app)

    # CORS(app)

    [api.add_resource(*route) for route in routes]
    return app
