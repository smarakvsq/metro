from flask import Blueprint, request, jsonify
from app.api.crime.util import validate_and_get_args

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
async def home():
    return "home"


@dashboard_blueprint.route("/dashboard_details")
@validate_and_get_args("transport_type", "weighted")
async def dashboard_details(body):
    transport_type = body.get("transport_type")
    weighted = body.get("weighted")

    data = {
        "call_for_service": {
            "total_calls": 1000,
            "previous_month": 900,
            "previous_year": 1500,
            "previous_month_percentage": 10,
            "previous_year_percentage": 20,
            "comment": "Placeholder for call_for_service comment",
        },
        "crime": {
            "boardings": 5,
            "crime_per_boardings": 10.2,
            "current_month": 120,
            "previous_month": 130,
            "previous_year": 1000,
            "previous_month_percentage": 5.2,
            "previous_year_percentage": 6.8,
            "comment": "Placeholder for crime comment",
        },
        "arrest": {
            "total_arrests": 500,
            "previous_month": 400,
            "previous_year": 1000,
            "previous_month_percentage": 10.00,
            "previous_year_percentage": 8.9,
            "comment": "Placeholder for arrest comment",
        },
    }
    return jsonify(data), 200
