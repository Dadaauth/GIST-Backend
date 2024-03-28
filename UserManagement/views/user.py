from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from StorageManagement.usermanagement import user

bp = Blueprint("user", __name__)


@bp.route("/all_users", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_users():
    users = user.get_all_users()
    return users[1], users[2]


@bp.route("/non_friends", methods=["GET"], strict_slashes=False)
@jwt_required()
def non_friends():
    users = user.get_non_friends(get_jwt_identity()['id'])
    return users[1], users[2]
