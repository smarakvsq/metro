from flask import Blueprint, jsonify, request

from app.api.call_for_service.cfs_utils import (
    get_call_for_service_agency_wide_bar,
    get_call_for_service_agency_wide_line,
    get_call_for_service_bar,
    get_call_for_service_comment,
    get_call_for_service_line,
    get_year_months,
)
from app.util import parse_date, validate_and_get_args

cfs_blueprint = Blueprint("call_for_service", __name__)


@cfs_blueprint.route("/call_for_service/data", methods=["POST"])
async def call_for_service_data():
    print("request body", request.json)
    call_for_service_data = []
    body = request.json
    graph_mapper = {"bar": get_call_for_service_bar, "line": get_call_for_service_line}

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    call_for_service_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(call_for_service_data), 200


@cfs_blueprint.route("/call_for_service/data/agency", methods=["POST"])
async def call_for_service_data_agency():
    print("request body", request.json)
    call_for_service_data = []
    body = request.json
    graph_mapper = {
        "bar": get_call_for_service_agency_wide_bar,
        "line": get_call_for_service_agency_wide_line,
    }

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        return jsonify({"Error": "dates field should be a list."})

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    call_for_service_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(call_for_service_data), 200


@cfs_blueprint.route("/call_for_service/comment", methods=["POST"])
async def get_section_comments():
    print("request body", request.json)
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
        comment = await get_call_for_service_comment(
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


@cfs_blueprint.route("/call_for_service/date_details")
@validate_and_get_args(published=True, transport_type=False)
async def get_date_details(body):
    year_months_obj_list = await get_year_months(
        published=body.get("published"), transport_type=body.get("transport_type")
    )
    year_months = [date_obj.strftime("%Y-%-m-%-d") for date_obj in year_months_obj_list]
    return jsonify(year_months), 200
