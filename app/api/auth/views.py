from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Forbidden, Unauthorized, NotFound, Conflict

from app.models.user import User
from app.metro_logging import app_logger as logger


auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")


@auth_blueprint.route('/auth/register', methods=['POST'])
async def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print("here")
    # Check if the user already exists
    existing_user: User = await User.get_by_username(username)
    
    logger.debug(existing_user)
    
    if existing_user:
        logger.debug(f"User exists. User created at {existing_user.created_at}")
        raise Conflict(f'Username {username} already exists')

    # Create a new user
    password_hash = generate_password_hash(password)
    new_user = await User.create(username=username, email=email, password_hash=password_hash)

    logger.info(f"New user {username} created.")
    
    # Log the user in
    return jsonify({'Message': 'User registered'})


@auth_blueprint.route('/auth/login', methods=['POST'])
async def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = await User.get_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        session.user_id = ""
        return jsonify({'message': 'Login Successful.'})
    
    raise Unauthorized('Invalid credentials')


@auth_blueprint.route('/auth/logout')
async def logout():
    "logout_user()"
    return jsonify({'message': 'Logout Successful'})


@auth_blueprint.route('/auth/reset_password', methods=['POST'])
async def reset_password():
    data = await request.get_json()
    email = data.get('email')
    user = await User.get_by_email(email)
    if user:
        # reset password here
        return jsonify({'message': 'Password reset instructions sent'})
    
    raise NotFound('User not found')

