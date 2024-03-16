from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models.User_Management.user import User


#TODO: Authenticate all database queries. Authenticate the source making those queries first
# Remember that soeone can easily sniff out information sent between the services so password based authentication
# might not be the best.

bp = Blueprint('usermanagement_main', __name__)

@bp.route('/create_user', methods=['POST'], strict_slashes=False)
def create_user():
    email = request.json.get('email', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    profile_pic_name = request.json.get('profile_pic_name', None)
    password = request.json.get('password', None)
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        profile_pic_name=profile_pic_name,
        password=password
    )
    new_user.save()
    return jsonify({"msg": "The user has been created successfully"}), 201

@bp.route('/user/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    """ Get a particular user based on an id"""
    user = User.search(id=user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user[0].to_dict())

@bp.route('/user/email/<user_email>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_by_email(user_email):
    """ Get a particular user based on their email"""
    user = User.search(email=user_email)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user[0].to_dict())

@bp.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_users():
    users = User.all()
    if len(users) == 0:
        return jsonify({'msg': "No users found"}), 404
    list_of_users = []
    for user in users:
        list_of_users.append(user.to_dict())
    return jsonify(list_of_users), 200
