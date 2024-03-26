from flask import Blueprint, request, jsonify
from app.util import validate_and_get_args, parse_date
from app.api.crime.schema import CrimeDetails
from flask_pydantic import validate


crime_blueprint = Blueprint("crime", __name__)


@crime_blueprint.route("/crime")
@validate_and_get_args(route=True, transport_type=False)
async def get_crime_category(params):

    data = ["On Person", "Property Related", "Society"]
    return jsonify(data), 200


@crime_blueprint.route("/crime/data")
@validate_and_get_args(
    route=True,
    transport_type=True,
    from_date=True,
    to_date=True,
    crime_type=True,
    crime_category=True,
    vetted=True,
    publish=True,
)
async def crime_data(body):
    print(body)
    # route = body.get("route")
    # transport_type = body.transport_type
    body["from_date"] = await parse_date(body.get("from_date"))
    body["to_date"] = await parse_date(body.get("to_date"))
    print(body)
    # crime_type = body.crime_type
    # crime_category = body.crime_category
    return jsonify({}), 200
