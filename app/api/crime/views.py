from flask import Blueprint, jsonify
from app.util import validate_and_get_args, parse_date
from app.api.crime.crime_utils import get_unique_ucr, get_crime_data, get_crime_data_agency


crime_blueprint = Blueprint("crime", __name__)


@crime_blueprint.route("/crime")
@validate_and_get_args(route=True, transport_type=False, vetted=True, severity=True)
async def get_crime_category(body):
    data = await get_unique_ucr(
        body.get("transport_type"),
        vetted=body.get("vetted"),
        severity=body.get("severity"),
    )
    return jsonify(data), 200


@crime_blueprint.route("/crime/data")
@validate_and_get_args(
    route_name=True,
    transport_type=False,
    from_date=True,
    to_date=True,
    severity=True,
    crime_category=True,
    vetted=True,
    published=True,
)
async def crime_data(body):
    print(body)
    crime_data = {}
    try:
        body["from_date"] = await parse_date(body.get("from_date"))
        body["to_date"] = await parse_date(body.get("to_date"))
        crime_data = await get_crime_data(body)
    except Exception as exc:
        jsonify({"Error": str(exc)}), 400

    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/data")
@validate_and_get_args(
    route_name=True,
    transport_type=False,
    from_date=True,
    to_date=True,
    severity=True,
    crime_category=True,
    vetted=True,
    published=True,
)
async def crime_data_agency(body):
    print(body)
    crime_data = {}
    try:
        body["from_date"] = await parse_date(body.get("from_date"))
        body["to_date"] = await parse_date(body.get("to_date"))
        crime_data = await get_crime_data_agency(body)
    except Exception as exc:
        jsonify({"Error": str(exc)}), 400

    return jsonify(crime_data), 200