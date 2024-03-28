import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from StorageManagement.usermanagement import friend as friend_s
from StorageManagement.contentmanagement import notify as notify_s

bp = Blueprint('friend', __name__)

@bp.route('/add_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_friend():
    """Sends a friend request to another user
    
    Method: POST
    Route: /add_friend

    Requirements:
        json:
            user_id, friend_id
    """
    user_id = get_jwt_identity()['id']
    friend_id = request.json.get('friend_id', None)
    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    
    response = friend_s.add_friend(user_id, friend_id)
    if response[0]:
        # send a notification to the friend
        notify_s.add_notification(friend_id, "friend requests", "Someone sent you a friend request")
    return jsonify({"msg": response[1]}), response[2]

@bp.route('/accept_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def accept_friend():
    """Accept a friend request
    
    Method: POST
    Route: /accept_friend

    Requirements:
        a logged in user
        json:
            friend_id

    Return: A message and a status code showing the result of the request
    """
    friend_id = request.json.get('friend_id', None)
    user = get_jwt_identity()

    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    
    response = friend_s.accept_friend(user['id'], friend_id=friend_id)
    
    if response[0]:
        # send a notification to the friend
        notify_s.add_notification(friend_id, "friend requests", 
                                  f"{user['first_name']} {user['last_name']} accepted your friend request"
                                  )
    return jsonify({"msg": response[1]}), response[2]

@bp.route('/friends', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friends():
    """Gets all the friends a particular user has
    
    Method: GET
    Route: /friends

    Requirements: A logged in user

    Return: a list of friends if successful else an error message   .....and a status code
    """
    response = friend_s.get_friends(get_jwt_identity()['id'])
    if not response[0]:
        return jsonify({"msg": response[1]}), response[2]
    return jsonify({"friends": response[1]}), response[2]

@bp.route('/friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friend_requests():
    """Gets all friend requests sent to the loggged in user
    
    Method: GET
    Route: /friend_requests

    Requirements: a logged in user
    Return: A jsonified list of friend requests.
    """
    response = friend_s.get_friend_requests(get_jwt_identity()['id'])
    if not response[0]:
        return jsonify({"msg": response[1]}), response[2]
    return response[1], response[2]

@bp.route('/sent_friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_sent_friend_requests():
    """Gets the friend requests a user has sent but is not accepted yet

    Method: GET
    Route: /sent_friend_requests

    Requirements: a logged in user
    Return: A jsonified list of friend requests
    """
    response = friend_s.get_sent_friend_requests(get_jwt_identity()['id'])
    if not response[0]:
        return jsonify({"msg": response[1]}), response[2]
    return jsonify({"sent friend requests": response[1]}), response[2]

@bp.route('/block/<friend_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def block(friend_id):
    """Blocks a particular friend
    
    Method: DELETE
    Route: /block/<friend_id>

    Requirements:
        a logged in user
        query parameters or route parameters:
            friend_id
    Return: success or error message
    """
    response = friend_s.block_friend(get_jwt_identity()['id'], friend_id)
    return jsonify({"msg": response[1]}), response[2]

# @bp.route('/unblock/<friend_id>', methods=['DELETE'], strict_slashes=False)
# @jwt_required()
# def unblock(friend_id):
#     response = requests.delete(
#         f'{storage_service_url}/usermanagement/friend/unblock/{friend_id}',
#         headers={"Authorization": request.headers.get('Authorization')}
#     )
#     return jsonify(response.json()), response.status_code

