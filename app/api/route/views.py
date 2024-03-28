from flask import Blueprint, request, jsonify
from app.util import validate_and_get_args
from app.api.route.route_utils import get_unique_lines

route_blueprint = Blueprint("route", __name__)


@route_blueprint.route("/routes/")
@validate_and_get_args(stat_type=True, transport_type=False, vetted=True)
async def get_routes(body):
    stat_type = body.get("stat_type")
    transport_type = body.get("transport_type")
    vetted = body.get("vetted")

    lines = []

    if transport_type:
        lines = await get_unique_lines(
            stat_type=stat_type, vetted=vetted, transport_type=transport_type
        )
        print(lines)

    return jsonify(lines), 200
