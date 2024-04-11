import os

from flask import Flask

from app.api import (arrest_blueprint, auth_blueprint, cfs_blueprint,
                     crime_blueprint, dashboard_blueprint, lp_admin_blueprint,
                     route_blueprint)
from app.constants import FilePath
from app.middleware import cors, handle_errors, log_request_response


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("metro_app")
    app.json.sort_keys = False
    create_dirs()
    app = register_middlewares(app)

    register_blueprints(app)

    return app


def register_blueprints(app):
    """register all blueprints for application"""
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(route_blueprint)
    app.register_blueprint(crime_blueprint)
    app.register_blueprint(arrest_blueprint)
    app.register_blueprint(cfs_blueprint)
    app.register_blueprint(lp_admin_blueprint)


def create_dirs():
    dir_paths = [FilePath.APP_LOG_PATH, FilePath.TASK_LOG_PATH]
    for dir_path in dir_paths:
        os.makedirs(dir_path, exist_ok=True)


def register_middlewares(app):
    app = log_request_response(app)
    app = handle_errors(app)
    cors(app)
    return app
