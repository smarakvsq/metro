from functools import wraps
from json import JSONDecodeError

from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized

from app.api.auth.auth_utils import decrypt_string
from app.models.user import User


def login_required(func):
    """Async decorator for Flask routes that require user authentication.

    Args:
        func (async def): The route function to be decorated.

    Returns:
        async def: The decorated async route function.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        uid = None
        try:
            data = request.json
            uid = data.get("uid")
        except (KeyError, JSONDecodeError) as e:
            raise BadRequest(f"Invalid request body: {e}") from e

        if not uid:
            raise BadRequest("Missing 'uid' in request body")

        user_id = str(await decrypt_string(uid), encoding="utf8")
        user = await User.get_by_id(user_id)

        if not user:
            raise BadRequest("User not found.")

        if not user.is_auth:
            raise Unauthorized("User not logged in.")

        # Call the decorated route function with authorized user object (optional)
        return await func(*args, **kwargs)

    return wrapper
