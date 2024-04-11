import sys
import traceback
from datetime import datetime
from functools import wraps

from flask import g, jsonify, make_response, request
from werkzeug.exceptions import HTTPException

from app.metro_logging import app_logger as logger


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


def log_request_response(app):
    @app.before_request
    def log_request():
        g.start_time = datetime.now()
        logger.info(f"Request: {request.method} {request.path}")
        if request.content_type == "application/json":
            logger.info(f"Request Body: {request.get_json()}")

    @app.after_request
    def log_response(response):
        end_time = datetime.now()
        logger.info(
            f"Response Status: {response.status_code} | Request Duration: {end_time - g.start_time} seconds"
        )
        return response

    return app


def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_all_exceptions(error):
        # Handle HTTP exceptions
        if isinstance(error, HTTPException):
            response = jsonify({"error": error.name, "message": error.description})
            response.status_code = error.code
            logger.error(f"HTTP Exception: {error.name} - {error.description}")
            return response

        # Handle other exceptions
        logger.error(f"Unexpected Error: {str(error.__class__)} | {str(error)}")
        logger.exception(traceback.format_exc())

        response = jsonify(
            {"error": "Internal Server Error", "message": "An unexpected error occurred."}
        )
        response.status_code = 500
        return response

    return app
