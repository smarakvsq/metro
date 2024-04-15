from flask import Blueprint, jsonify, request

from app.auth import login_required
from app.metro_logging import app_logger as logger

lp_admin_blueprint = Blueprint("landing_admin", __name__)


@lp_admin_blueprint.route("/dashboard/comments", methods=["POST"])
@login_required
async def update_landing_comments():
    body = request.json
    logger.debug(f"Req body: {body}")
    return jsonify(body)
