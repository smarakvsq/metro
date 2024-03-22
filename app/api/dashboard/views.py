from flask import Blueprint, request, jsonify
from app.util import validate_and_get_args
from app.api.dashboard.prepare_dashboard_data import (
    get_arrest_data,
    get_call_for_service_data,
    get_crime_data,
)

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
async def home():
    return "home"


@dashboard_blueprint.route("/dashboard_details")
@validate_and_get_args("transport_type", "published")
async def dashboard_details(body):
    transport_type = body.get("transport_type")
    published = body.get("published")

    arrest = await get_arrest_data(transport_type=transport_type, published=published)
    call_for_service = await get_call_for_service_data(
        transport_type=transport_type, published=published
    )
    crime = await get_crime_data(transport_type=transport_type, published=published)

    data = {"call_for_service": call_for_service, "crime": crime, "arrest": arrest}
    return jsonify(data), 200
