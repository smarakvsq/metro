from flask import Blueprint, request, jsonify
from app.util import validate_and_get_args

route_blueprint = Blueprint("route", __name__)


@route_blueprint.route("/routes/")
@validate_and_get_args("type", "transport_type")
async def get_routes(body):
    stat_type = body.get("type")
    transport_type = body.get("transport_type")

    data = [
        {"route_name": "Route A", "route_id": 1},
        {"route_name": "Route B", "route_id": 2},
    ]
    return jsonify(data), 200
