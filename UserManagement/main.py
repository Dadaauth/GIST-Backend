from flask import Blueprint

from .views.auth import bp as auth_bp
from .views.friend import bp as friend_bp
from .views.user import bp as user_bp

bp = Blueprint("usermanagement", __name__)

bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(friend_bp, url_prefix='/friend')
bp.register_blueprint(user_bp, url_prefix='/user')