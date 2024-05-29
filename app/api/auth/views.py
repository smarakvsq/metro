from flask import Blueprint, jsonify, request, session
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized, UnprocessableEntity
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.auth.auth_utils import decrypt_string, encrypt_string
from app.metro_logging import app_logger as logger
from app.models.user import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")


@auth_blueprint.route("/auth/register", methods=["POST"])
async def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    # Check if the user already exists
    existing_user: User = await User.get_by_username(username)

    logger.debug(existing_user)

    if existing_user:
        logger.debug(f"User exists. User created at {existing_user.created_at}")
        raise Conflict(f"Username {username} already exists")

    # Create a new user
    password_hash = generate_password_hash(password)
    try:
        new_user = await User.create(username=username, email=email, password_hash=password_hash)
    except Exception as exc:
        logger.exception(exc)
        raise

    if new_user:
        logger.info(f"New user {username} created.")
        return jsonify({"Message": "User registered"})

    logger.info(f"Failed to create new user.")
    raise UnprocessableEntity("Failed to create new user")


@auth_blueprint.route("/auth/login", methods=["POST"])
async def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username and password:
        raise BadRequest("Provide username/password.")

    user = await User.get_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        enc = await encrypt_string(str(user.id))
        await user.update(is_auth=True)
        return jsonify({"Message": "Login Successful.", "uid": str(enc, encoding="utf8")})

    raise Unauthorized("Invalid credentials")


@auth_blueprint.route("/auth/logout", methods=["POST"])
async def logout():
    body = request.json
    enc_user = body.get("uid")
    if enc_user:
        user_id = await decrypt_string(enc_user)
        logger.debug(f"User ID: {user_id}")
        user = await User.get_by_id(str(user_id, encoding="utf8"))
        if user:
            await user.update(is_auth=False)
            return jsonify({"Message": "Logout Successful"})
        raise BadRequest("User not found.")
    raise Unauthorized("User not logged in.")


@auth_blueprint.route("/auth/reset_password", methods=["POST"])
async def reset_password():
    data = await request.get_json()
    email = data.get("email")
    user = await User.get_by_email(email)
    if user:
        # reset password here
        return jsonify({"Message": "Password reset instructions sent"})

    raise NotFound("User not found")
