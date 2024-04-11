from flask import Blueprint, jsonify, request

from app.api.arrest.arrest_utils import (get_arrest_agency_wide_bar,
                                         get_arrest_agency_wide_line,
                                         get_arrest_comment, get_arrest_line,
                                         get_arrest_pie, get_year_months)
from app.util import parse_date, validate_and_get_args

arrest_blueprint = Blueprint("arrest", __name__)


@arrest_blueprint.route("/arrest/data", methods=["POST"])
async def arrest_data():
    arrest_data = []
    body = request.json
    graph_mapper = {"pie": get_arrest_pie, "line": get_arrest_line}

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    arrest_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(arrest_data), 200


@arrest_blueprint.route("/arrest/data/agency", methods=["POST"])
async def arrest_data_agency():
    arrest_data = []
    body = request.json
    graph_mapper = {"bar": get_arrest_agency_wide_bar, "line": get_arrest_agency_wide_line}

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    arrest_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(arrest_data), 200


@arrest_blueprint.route("/arrest/comment", methods=["POST"])
async def get_section_comments():
    body = request.json
    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."}), 400

    if len(body.get("dates")) != 1:
        return (
            jsonify(
                {
                    "comments": "",
                    "message": f"Number of months are {len(body.get('dates'))}. Comments available only for single month selection.",
                }
            ),
            200,
        )
    year_month = await parse_date(body.get("dates")[0])

    comment = ""
    try:
        comment = await get_arrest_comment(
            line_name=body.get("line_name"),
            transport_type=body.get("transport_type"),
            section_heading=body.get("section"),
            year_month=year_month,
            published=body.get("published"),
        )
    except Exception as exc:
        print(exc)
        return jsonify({"Error": str(exc)}), 400

    return jsonify({"comment": comment}), 200


@arrest_blueprint.route("/arrest/date_details")
@validate_and_get_args(published=True, transport_type=False)
async def get_date_details(body):
    year_months_obj_list = await get_year_months(
        published=body.get("published"), transport_type=body.get("transport_type")
    )
    year_months = [date_obj.strftime("%Y-%-m-%-d") for date_obj in year_months_obj_list]
    return jsonify(year_months), 200
