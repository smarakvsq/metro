from flask import Blueprint, jsonify
from app.util import validate_and_get_args, parse_date
from app.api.crime.crime_utils import (
    get_unique_ucr,
    get_crime_data_bar,
    get_crime_data_line,
    get_crime_data_agency_bar,
    get_crime_data_agency_line,
    get_year_months_for_comment,
    get_crime_comment,
)

crime_blueprint = Blueprint("crime", __name__)


@crime_blueprint.route("/crime")
@validate_and_get_args(line_name=False, transport_type=False, vetted=True, severity=True)
async def get_crime_category(body):
    print("request body", body)
    data = await get_unique_ucr(
        line_name=body.get("line_name"),
        transport_type=body.get("transport_type"),
        vetted=body.get("vetted"),
        severity=body.get("severity"),
    )
    return jsonify(data), 200


@crime_blueprint.route("/crime/data")
@validate_and_get_args(
    line_name=False,
    transport_type=False,
    from_date=True,
    to_date=True,
    severity=True,
    crime_category=False,
    vetted=True,
    published=True,
    graph_type=True,
)
async def crime_data(body):
    print("request body", body)
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_data_bar,
        "line": get_crime_data_line,
    }
    body["from_date"] = await parse_date(body.get("from_date"))
    body["to_date"] = await parse_date(body.get("to_date"))
    crime_data = await graph_mapper[body.get("graph_type")](body)
    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/data/agency")
@validate_and_get_args(
    line_name=False,
    transport_type=False,
    from_date=True,
    to_date=True,
    severity=True,
    crime_category=False,
    vetted=True,
    published=True,
    graph_type=True,
)
async def crime_data_agency(body):
    print(body)
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_data_agency_bar,
        "line": get_crime_data_agency_line,
    }
    try:
        body["from_date"] = await parse_date(body.get("from_date"))
        body["to_date"] = await parse_date(body.get("to_date"))
        crime_data = await graph_mapper[body.get("graph_type")](body)
    except Exception as exc:
        jsonify({"Error": str(exc)}), 400

    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/comment")
@validate_and_get_args(
    line_name=False,
    transport_type=False,
    from_date=True,
    to_date=True,
    section=True,
    vetted=True,
    published=True,
    crime_category=False,
)
async def get_section_comments(body):
    body["from_date"] = await parse_date(body.get("from_date"))
    body["to_date"] = await parse_date(body.get("to_date"))
    year_months = await get_year_months_for_comment(body)
    if len(year_months) != 1:
        return jsonify(
            {
                "comments": "",
                "message": f"Number of months are {len(year_months)}. Comments available only for single month selection.",
            }
        )
    year_month = year_months[0]
    comment = ""
    try:
        comment = await get_crime_comment(
            vetted=body.get("vetted"),
            line_name=body.get("line_name"),
            transport_type=body.get("transport_type"),
            section_heading=body.get("section"),
            sub_section_heading=body.get("crime_category"),
            year_month=year_month,
            published=body.get("published")
        )
    except Exception as exc:
        print(exc)
        return jsonify({"Error": str(exc)}), 400

    return jsonify({"comment": comment}), 200
