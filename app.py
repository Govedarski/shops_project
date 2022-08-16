from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
configuration = config("CONFIGURATION")
app.config.from_object(configuration)

api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.after_request
def return_response(response):
    db.session.commit()
    return response


[api.add_resource(*route_data) for route_data in routes]

if __name__ == '__main__':
    app.run()
