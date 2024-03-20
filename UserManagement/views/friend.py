from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

bp = Blueprint('friend', __name__)

storage_service_url = "http://127.0.0.1:5001/api/v1.0/storagemanagement/"
storage_service_url_production = "https://socialnet.clementauthority.me/api/v1.0/storagemanagement/"

@bp.route('/add_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_friend():
    friend_id = request.json.get('friend_id', None)

    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    response = requests.post(
        f'{storage_service_url}/usermanagement/friend/add_friend',
        json=request.json,
        headers={"Authorization": request.headers.get('Authorization')}
    )
    if response.status_code not in {400, 404, 500, 501}:
        # send a notification to the friend
        requests.post(
            f"{storage_service_url}/contentmanagement/notify/add_notification",
            json={
                "user_id": friend_id,
                "type": "friend requests",
                "content": "Someone sent you a friend request"
            },
            headers={"Authorization": request.headers.get('Authorization')}
        )
    return jsonify(response.json()), response.status_code

@bp.route('/accept_friend', methods=['POST'], strict_slashes=False)
@jwt_required()
def accept_friend():
    friend_id = request.json.get('friend_id', None)
    user = get_jwt_identity()

    if friend_id is None:
        return jsonify({'msg': 'friend_id is not present in request'}), 400
    response = requests.post(
        f'{storage_service_url}/usermanagement/friend/accept_friend',
        json=request.json,
        headers={"Authorization": request.headers.get('Authorization')}
    )
    if response.status_code not in {400, 404, 500, 501}:
        # send a notification to the friend
        requests.post(
            f"{storage_service_url}/contentmanagement/notify/add_notification",
            json={
                "user_id": friend_id,
                "type": "friend requests",
                "content": f"{user['first_name']} {user['last_name']} accepted your friend request"
            },
            headers={"Authorization": request.headers.get('Authorization')}
        )
    return jsonify(response.json()), response.status_code

@bp.route('/friends', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friends():
    response = requests.get(
        f'{storage_service_url}/usermanagement/friend/friends',
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@bp.route('/friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_friend_requests():
    response = requests.get(
        f'{storage_service_url}/usermanagement/friend/friend_requests',
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@bp.route('/sent_friend_requests', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_sent_friend_requests():
    response = requests.get(
        f'{storage_service_url}/usermanagement/friend/sent_friend_requests',
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@bp.route('/block/<friend_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def block(friend_id):
    response = requests.delete(
        f'{storage_service_url}/usermanagement/friend/block/{friend_id}',
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code