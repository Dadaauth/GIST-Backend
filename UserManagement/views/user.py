from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from StorageManagement.usermanagement import user

bp = Blueprint("user", __name__)


@bp.route('/get_user/<user_id>', methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    """Gets a particular user details from storage based on <user_id>
    
    Method: GET
    Route: /get_user/<user_id>


    Requirements:
        query params or route params:
            user_id: the id of the user whose information is needed

    Return: an object representation of the user
    """
    user_g = user.get_user(user_id)
    return user_g[1], user_g[2]


@bp.route("/all_users", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_users():
    """Gets all the users in storage

    Return: all users in storage and an http status code.
    """
    users = user.get_all_users()
    return users[1], users[2]


@bp.route("/non_friends", methods=["GET"], strict_slashes=False)
@jwt_required()
def non_friends():
    """Gets all user in storage that are not the logged in user's friend

    Return: all users in storage that are not the logged in user friend
    """
    users = user.get_non_friends(get_jwt_identity()['id'])
    return users[1], users[2]
