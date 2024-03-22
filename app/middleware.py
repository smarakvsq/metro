from flask import Flask, request, make_response
from functools import wraps
from datetime import timedelta


def cors(app):
    """
    A function that enables CORS for a Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.before_request
    def before_request_cors():
        if request.method == "OPTIONS":
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Max-Age": "3600",
            }
            response = make_response("", 204, headers)
            return response

    @app.after_request
    def after_request_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response
