from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Forbidden, Unauthorized, NotFound

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
    print(existing_user)
    if existing_user:
        logger.debug(f"User exists. User created at {existing_user.created_at}")
        raise Forbidden(f'Username {username} already exists')

    # Create a new user
    password_hash = generate_password_hash(password)
    new_user = await User.create(username=username, email=email, password_hash=password_hash)

    logger.info(f"New user {username} created.")
    
    # Log the user in
    await login_user(new_user)
    logger.info(f"Login new user {username}.")
    return jsonify({'message': 'User registered and logged in'})


@auth_blueprint.route('/auth/login', methods=['POST'])
async def login():
    data = await request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = await User.get_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Login Successful.'})
    
    raise Unauthorized('Invalid credentials')


@auth_blueprint.route('/auth/logout')
@login_required
async def logout():
    logout_user()
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

