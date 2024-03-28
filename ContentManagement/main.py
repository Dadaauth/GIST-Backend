from flask import Blueprint

from .views.posts import bp as posts_bp

bp = Blueprint("contentmanagement", __name__)

bp.register_blueprint(posts_bp, url_prefix='/posts')
