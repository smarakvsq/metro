from flask import Blueprint, jsonify, request

from app.api.crime.crime_utils import (
    get_crime_comment,
    get_crime_data_agency_bar,
    get_crime_data_agency_line,
    get_crime_data_bar,
    get_crime_data_line,
    get_unique_ucr,
    get_year_months,
)
from app.util import parse_date, validate_and_get_args

crime_blueprint = Blueprint("crime", __name__)


@crime_blueprint.route("/crime")
@validate_and_get_args(line_name=False, transport_type=False, vetted=True, severity=False)
async def get_crime_category(body):
    print("request body", body)
    data = await get_unique_ucr(
        line_name=body.get("line_name"),
        transport_type=body.get("transport_type"),
        vetted=body.get("vetted"),
        severity=body.get("severity"),
    )
    return jsonify(data), 200


@crime_blueprint.route("/crime/data", methods=["POST"])
async def crime_data():
    print("request body", request.json)
    body = request.json
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_data_bar,
        "line": get_crime_data_line,
    }
    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    crime_data = await graph_mapper[body.get("graph_type")](body)
    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/data/agency", methods=["POST"])
async def crime_data_agency():
    print("request body", request.json)
    body = request.json
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_data_agency_bar,
        "line": get_crime_data_agency_line,
    }

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    crime_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/comment", methods=["POST"])
async def get_section_comments():
    print("request body", request.json)
    body = request.json

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."}), 400

    if len(body.get("dates")) != 1:
        return jsonify(
            {
                "comments": "",
                "message": f"Number of months are {len(body.get('dates'))}. Comments available only for single month selection.",
            }
        )
    year_month = await parse_date(body.get("dates")[0])

    comment = ""
    try:
        comment = await get_crime_comment(
            vetted=body.get("vetted"),
            line_name=body.get("line_name"),
            transport_type=body.get("transport_type"),
            section_heading=body.get("section"),
            sub_section_heading=body.get("crime_category"),
            year_month=year_month,
            published=body.get("published"),
        )
    except Exception as exc:
        print(exc)
        return jsonify({"Error": str(exc)}), 400

    return jsonify({"comment": comment}), 200


@crime_blueprint.route("/crime/date_details")
@validate_and_get_args(vetted=True, published=True, transport_type=False)
async def get_date_details(body):
    year_months_obj_list = await get_year_months(
        vetted=body.get("vetted"),
        published=body.get("published"),
        transport_type=body.get("transport_type"),
    )
    year_months = [date_obj.strftime("%Y-%-m-%-d") for date_obj in year_months_obj_list]
    return jsonify(year_months), 200
