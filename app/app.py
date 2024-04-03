from flask import Flask
from flask_migrate import Migrate

from app.api import (arrest_blueprint, cfs_blueprint, crime_blueprint,
                     dashboard_blueprint, route_blueprint)
from app.middleware import cors


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("metro_app")
    cors(app)
    # app.config.from_object("app.config")

    register_blueprints(app)
    # app_setup(app)

    return app


def register_blueprints(app):
    """register all blueprints for application"""
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(route_blueprint)
    app.register_blueprint(crime_blueprint)
    app.register_blueprint(arrest_blueprint)
    app.register_blueprint(cfs_blueprint)


# def app_setup(app):
# migrate = Migrate()
# migrate.init_app(app, engine)
