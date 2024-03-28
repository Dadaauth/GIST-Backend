from flask import Blueprint

from .views.chat import bp as chat_bp

bp = Blueprint("chatnotificationfeed", __name__)

bp.register_blueprint(chat_bp, url_prefix='/chat')
