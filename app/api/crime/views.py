from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from app.api.crime.crime_utils import (
    get_crime_comment,
    get_crime_data_agency_bar,
    get_crime_data_agency_line,
    get_crime_data_bar,
    get_crime_data_line,
    get_unique_ucr,
    get_year_months,
)
from app.api.crime.unvetted_utils import (
    get_crime_unvetted_data_agency_bar,
    get_crime_unvetted_data_agency_line,
    get_crime_unvetted_data_bar,
    get_crime_unvetted_data_line,
    get_unvetted_crime_comment,
    get_unvetted_date,
)
from app.constants import CrimeSeverity
from app.metro_logging import app_logger as logger
from app.util import get_year_month_week, parse_date, validate_and_get_args

crime_blueprint = Blueprint("crime", __name__)


@crime_blueprint.route("/crime")
@validate_and_get_args(line_name=False, transport_type=False, vetted=True, severity=False)
async def get_crime_category(body):
    data = await get_unique_ucr(
        line_name=body.get("line_name"),
        transport_type=body.get("transport_type"),
        vetted=body.get("vetted"),
        severity=body.get("severity"),
    )
    return jsonify(data), 200


@crime_blueprint.route("/crime/data", methods=["POST"])
async def crime_data():
    body = request.json
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_data_bar,
        "line": get_crime_data_line,
    }
    if not body.get("dates") and not isinstance(body.get("dates"), list):
        raise BadRequest("Dates field should be a list.")

    if (
        body.get("severity")
        and body.get("severity") == CrimeSeverity.VIOLENT_CRIME
        and body.get("crime_category")
    ):
        raise BadRequest(
            f'Input crime_category and severity {body.get("severity")} are mutually exclusive.'
        )

    body["dates"] = [await parse_date(x) for x in body.get("dates")]
    crime_data = await graph_mapper[body.get("graph_type")](body)
    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/data/agency", methods=["POST"])
async def crime_data_agency():
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
    body = request.json

    if not body.get("dates") and not isinstance(body.get("dates"), list):
        raise BadRequest("dates field should be a list.")

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
        logger.exception(exc)
        raise UnprocessableEntity(str(exc))

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


@crime_blueprint.route("/crime/unvetted/date")
@validate_and_get_args(published=True, transport_type=False)
async def crime_unvetted(body):
    year_month_week = await get_unvetted_date(
        published=body.get("published"),
        transport_type=body.get("transport_type"),
    )
    return jsonify(year_month_week), 200


@crime_blueprint.route("/crime/unvetted/data", methods=["POST"])
async def crime_data_unvetted():
    body = request.json
    crime_unvetted_data = {}
    graph_mapper = {
        "bar": get_crime_unvetted_data_bar,
        "line": get_crime_unvetted_data_line,
    }

    if not body.get("dates"):
        raise BadRequest("Dates unavailable.")

    if not isinstance(body.get("dates"), dict):
        raise BadRequest("Dates field should be a dictionary of dates and weeks.")

    if (
        body.get("severity")
        and body.get("severity") == CrimeSeverity.VIOLENT_CRIME
        and body.get("crime_category")
    ):
        raise BadRequest(
            f'Input crime_category and severity {body.get("severity")} are mutually exclusive.'
        )

    year_months, weeks = await get_year_month_week(body.pop("dates"))
    body["year_months"] = year_months
    body["weeks"] = weeks
    crime_unvetted_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(crime_unvetted_data), 200


@crime_blueprint.route("/crime/unvetted/data/agency", methods=["POST"])
async def crime_data_unvetted_agency():
    body = request.json
    crime_data = {}
    graph_mapper = {
        "bar": get_crime_unvetted_data_agency_bar,
        "line": get_crime_unvetted_data_agency_line,
    }

    if not body.get("dates"):
        raise BadRequest("Dates unavailable.")

    if not isinstance(body.get("dates"), dict):
        raise BadRequest("Dates field should be a dictionary of dates and weeks.")

    year_months, weeks = await get_year_month_week(body.pop("dates"))
    body["year_months"] = year_months
    body["weeks"] = weeks
    crime_data = await graph_mapper[body.get("graph_type")](body)

    return jsonify(crime_data), 200


@crime_blueprint.route("/crime/unvetted/comment", methods=["POST"])
async def get_unetted_section_comments():
    body = request.json

    await get_unvetted_crime_comment(
        vetted=body.get("vetted"),
        line_name=body.get("line_name"),
        transport_type=body.get("transport_type"),
        section_heading=body.get("section"),
        sub_section_heading=body.get("crime_category"),
        year_month="year_month",
        published=body.get("published"),
    )

    return jsonify({"comment": ""}), 200
