from flask import Blueprint, jsonify, request

from app.auth import login_required
from app.constants import PageType
from app.comment_constants import LandingSectionHeading
from app.metro_logging import app_logger as logger
from app.util import is_valid_value
from werkzeug.exceptions import BadRequest, UnprocessableEntity

lp_admin_blueprint = Blueprint("landing_admin", __name__, url_prefix="admin")


@lp_admin_blueprint.route("/admin/comments", methods=["POST"])
@login_required
async def update_comments():
    body = request.json

    comment_info = body.get("comment_info")

    if not isinstance(body, comment_info):
        raise BadRequest("comment_info should be a list.")

    # section_name = body.get("section")
    # sub_section_name = body.get("sub_section")
    page_type = body.get("stat_type")
    line_name = body.get("line_name")
    transport_type = body.get("transport_type")
    year_month = body.get("dates")

    if not year_month:
        raise BadRequest("Provide date.")

    if not isinstance(year_month, list):
        raise BadRequest("Dates should be a list")
    
    if len(year_month) > 1:
        raise UnprocessableEntity("Dates should be singular for updation.")

    return jsonify(body)
