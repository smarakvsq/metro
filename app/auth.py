from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
async def load_user(user_id):
    from app.api.models import User

    return await User.get_by_id(user_id)
