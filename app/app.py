from flask import Flask
from app.api import dashboard_blueprint, route_blueprint, crime_blueprint


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("metro_app")
    # app.config.from_object("app.config")

    register_blueprints(app)

    return app


def register_blueprints(app):
    """register all blueprints for application"""
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(route_blueprint)
    app.register_blueprint(crime_blueprint)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
